"""Read-only SCFA package scanner. Python standard library; no game writes.

Usage: python tools/scan_scfa_maps.py --maps <package> --game <Steam FA> --out <report.json>
This is a static triage tool. It does not establish playability or resolve dynamic imports.
"""
from pathlib import Path
import argparse
import collections
from functools import lru_cache
import hashlib
import json
import re
import zipfile


def read(path):
    raw = path.read_bytes()
    if raw.startswith(b'\x1bLua'):
        return None
    for encoding in ('utf-8-sig', 'gb18030', 'cp1252'):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            pass
    return raw.decode('utf-8', 'replace')


def strip_comments(source):
    # Preserve quoted/long strings and source line numbers. # is a comment in retail FA Lua.
    pattern = re.compile(r'"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|--\[(=*)\[.*?\]\1\]|--[^\n]*|\#[^\n]*|\[(=*)\[.*?\]\2\]', re.S)
    return pattern.sub(lambda m: re.sub(r'[^\n]', ' ', m[0]) if m[0].startswith(('--', '#')) else m[0], source)


def scan(maps, game):
    assets = set()
    units = set()
    for package in (game / 'gamedata').glob('*.scd'):
        with zipfile.ZipFile(package) as archive:
            for name in archive.namelist():
                key = name.replace('\\', '/').lower().lstrip('/')
                assets.add(key)
                if key.startswith('schook/'):
                    assets.add(key[7:])
                if key.endswith('_unit.bp'):
                    units.add(Path(key).name[:-8])
    if not assets:
        raise ValueError('No Steam gamedata/*.scd found; refusing an empty asset baseline')
    folders = collections.defaultdict(list)
    scenarios = sorted(p for p in maps.rglob('*_scenario.lua') if '.git' not in p.parts)
    for scenario in scenarios:
        folders[scenario.parent.name.lower()].append(scenario.parent)

    @lru_cache(maxsize=None)
    def local_files(folder):
        return {p.relative_to(folder).as_posix().lower() for p in folder.rglob('*') if p.is_file()}

    def resolve(ref, owner):
        key = ref.replace('\\', '/').lower().lstrip('/')
        if key in assets:
            return 'steam'
        if key.startswith('maps/'):
            parts = key.split('/', 2)
            if len(parts) == 3:
                choices = [owner] if owner.name.lower() == parts[1] else folders.get(parts[1], [])
                for folder in choices:
                    if parts[2] in local_files(folder):
                        return 'self' if folder == owner else 'other-map'
                if (game / key).is_file():
                    return 'official-map'
        return 'not-found-static'

    records = []
    for scenario in scenarios:
        folder = scenario.parent
        row = {'folder': folder.relative_to(maps).as_posix(), 'scenario': scenario.name,
               'files': [], 'imports': [], 'scmap_assets': [], 'bytecode': [], 'candidate_flags': []}
        for path in sorted(folder.rglob('*')):
            if not path.is_file() or '.git' in path.relative_to(folder).parts:
                continue
            rp = path.relative_to(folder).as_posix()
            raw = path.read_bytes()
            row['files'].append({'path': rp, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
            if path.suffix.lower() == '.scmap':
                for mt in re.finditer(rb'[\x20-\x7e]{6,}', raw):
                    ref = mt[0].decode('ascii')
                    if re.match(r'^/?(?:env|textures|maps|effects|props)/', ref, re.I) and re.search(r'\.(?:dds|bp|scm|sfx)$', ref, re.I):
                        row['scmap_assets'].append({'file': rp, 'offset': mt.start(), 'ref': ref, 'resolution': resolve(ref, folder)})
            if path.suffix.lower() not in ('.lua', '.luac'):
                continue
            source = read(path)
            if source is None:
                row['bytecode'].append(rp)
                continue
            source = strip_comments(source)
            for mt in re.finditer(r"\b(?:import|doscript)\s*\(\s*(['\"])([^'\"\r\n]+)\1\s*\)", source):
                row['imports'].append({'file': rp, 'line': source.count('\n', 0, mt.start()) + 1,
                                       'ref': mt[2], 'resolution': resolve(mt[2], folder)})
            flags = {
                'module-vs-global-api': r'\bScenarioFramework\.SetIgnorePlayableRect\s*\(',
                'lua50-vararg-forwarding': r'(?:,\s*|\(\s*)\.\.\.\s*\)',
                'review-sim-ui-boundary': r"import\s*\(['\"]/lua/ui/",
                'review-random-determinism': r'\bmath\.random\s*\(',
            }
            for kind, pattern in flags.items():
                for mt in re.finditer(pattern, source):
                    row['candidate_flags'].append({'kind': kind, 'file': rp, 'line': source.count('\n', 0, mt.start()) + 1})
        records.append(row)
    return {'map_count': len(records), 'steam_assets': len(assets), 'steam_unit_count': len(units),
            'game_started': False, 'limitations': ['literal imports only', 'ASCII SCMAP path extraction, not a complete format parser',
                                                 'flags require call-path review', 'no Lua compilation or game simulation'],
            'folder_collisions': {k: [p.relative_to(maps).as_posix() for p in v] for k, v in folders.items() if len(v) > 1},
            'maps': records}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--maps', type=Path, required=True)
    parser.add_argument('--game', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error('--out already exists; use a new report path to preserve evidence')
    report = scan(args.maps.resolve(), args.game.resolve())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Static scan: {report['map_count']} maps; {report['steam_unit_count']} retail blueprints; game not started")
