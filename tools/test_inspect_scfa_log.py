"""Parser boundary tests; fixtures are synthetic, not actual game evidence."""
import unittest
from pathlib import Path
import subprocess
import sys
import tempfile
from inspect_scfa_log import inspect


class LogInspectionTests(unittest.TestCase):
    def test_native_error_context_and_order(self):
        raw = b"info: Survival MOD: Configuring match settings...\nwarning: bad argument to AddBuildRestriction\n stack traceback:\n ScenarioFramework.lua:949\n map_script.lua:1084\n"
        result = inspect(raw)
        self.assertEqual(result["stage_lines"]["configure"], [1])
        self.assertEqual(result["stage_lines"]["markers"], [])
        self.assertEqual(result["error_pattern_lines"], [2, 3])
        self.assertEqual([x["line"] for x in result["contexts"][0]], [1,2,3,4,5])
        self.assertEqual(result["status"], "observations_only_root_cause_unconfirmed")

    def test_plain_blueprint_name_is_only_a_clue(self):
        result = inspect(b"info: checking uaa0314\n")
        self.assertEqual(result["error_pattern_lines"], [])
        self.assertEqual(result["clue_pattern_lines"], [1])

    def test_empty_log_cannot_prove_success(self):
        result = inspect(b"")
        self.assertEqual(result["contexts"], [])
        self.assertTrue(all(not value for value in result["stage_lines"].values()))
        self.assertIn("unconfirmed", result["status"])

    def test_encodings(self):
        for encoding in ("utf-8-sig", "utf-16", "gb18030"):
            result = inspect("中文 error score.lua".encode(encoding))
            self.assertEqual(result["error_pattern_lines"], [1])
            self.assertIn("中文", result["contexts"][0][0]["text"])

    def test_limit_marks_truncation(self):
        result = inspect(b"error\n"*10, context=0, limit=2)
        self.assertTrue(result["context_truncated"])
        self.assertEqual(len(result["error_pattern_lines"]), 10)

    def test_cli_refuses_to_overwrite_source_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            log = Path(folder)/"original.log"
            raw = b"error score.lua\n"
            log.write_bytes(raw)
            run = subprocess.run([sys.executable, str(Path(__file__).with_name("inspect_scfa_log.py")), str(log), "--out", str(log)], capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertEqual(log.read_bytes(), raw)


if __name__ == "__main__":
    unittest.main()
