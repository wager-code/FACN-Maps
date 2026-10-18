"""Read an existing SCFA log; report observations, never infer a root cause.

No Lua execution, game writes or automatic repair. Context is local diagnostic
data and may contain user paths. Review it before sharing publicly.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re


STAGES = {
    "populate": "Survival MOD: OnPopulate()",
    "configure": "Survival MOD: Configuring match settings",
    "markers": "Survival MOD: Initializing marker lists",
    "objective": "Survival MOD: Initializing defense object",
    "prebuild": "Survival MOD: Initializing prebuild objects",
    "start": "Survival MOD: Initializing game start sequence",
    "tick": "Survival MOD: Tick thread started",
}
ERROR = re.compile(r"\b(?:error|exception)\b|stack traceback|bad argument|attempt to (?:call|index|perform)", re.I)
CLUES = re.compile(r"uaa0314|AddBuildRestriction|ScenarioFramework|OnPopulate|score\.lua|scoreaccum|Fort.?Ictus", re.I)


def decode(raw):
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16"), "utf-16"
    for encoding in ("utf-8-sig", "gb18030"):
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            pass
    return raw.decode("latin1"), "latin1"


def inspect(raw, context=4, limit=40):
    source, encoding = decode(raw)
    lines = source.splitlines()
    errors = [i for i, line in enumerate(lines) if ERROR.search(line)]
    clues = [i for i, line in enumerate(lines) if CLUES.search(line)]
    selected = sorted(set(errors + clues))[:limit]
    spans = []
    for index in selected:
        start, end = max(0, index-context), min(len(lines), index+context+1)
        if spans and start <= spans[-1][1]:
            spans[-1][1] = max(spans[-1][1], end)
        else:
            spans.append([start, end])
    return {
        "status": "observations_only_root_cause_unconfirmed",
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw), "encoding": encoding, "line_count": len(lines),
        "stage_lines": {name: [i+1 for i,line in enumerate(lines) if text in line]
                        for name,text in STAGES.items()},
        "error_pattern_lines": [i+1 for i in errors],
        "clue_pattern_lines": [i+1 for i in clues],
        "context_truncated": len(set(errors+clues)) > limit,
        "contexts": [[{"line": i+1, "text": lines[i]} for i in range(start,end)]
                     for start,end in spans],
        "limits": "Pattern hits are leads, not proof. Missing markers may mean a different map, incomplete logging or an early failure. Replay headers and offline Lua stubs do not prove runtime diplomacy or native API errors.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("--out", type=Path, help="New JSON file; refuses to overwrite an existing file")
    args = parser.parse_args()
    result = inspect(args.log.read_bytes())
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        # Exclusive creation also prevents accidentally overwriting the input log.
        with args.out.open("x", encoding="utf-8") as stream:
            stream.write(output + "\n")
        print(f"Saved observations: {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()
