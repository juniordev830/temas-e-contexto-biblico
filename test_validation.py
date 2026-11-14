import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from app import run

ROOT = Path(__file__).resolve().parent

class InputValidationTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))

    def test_root_must_be_object(self):
        for value in (None, [], "texto", 3, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                run(value)

    def test_valid_input_is_not_mutated(self):
        original = copy.deepcopy(self.data)
        run(self.data)
        self.assertEqual(self.data, original)

    def test_invalid_json_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invalid.json"
            path.write_text('{"incompleto":', encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "app.py"), str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_file_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(ROOT / "app.py"), str(Path(tmp) / "missing.json")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)

    def test_collection_requires_objects(self):
        for value in ({}, None, "", 42, [None], ["texto"], [[]], [True]):
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data['passagens'] = value
                with self.assertRaises(ValueError):
                    run(data)

    def test_invalid_collection_cli(self):
        self.data['passagens'] = {}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invalid.json"
            path.write_text(json.dumps(self.data), encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "app.py"), str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)
