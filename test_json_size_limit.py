"""Limita leitura de JSON na entrada padrão antes de desserializar."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parent


class InputSizeLimitTests(unittest.TestCase):
    def test_oversized_stdin_is_rejected(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "app.py"), "-"],
            input=b" " * 1_000_001,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"limite de 1 MB", result.stderr)
        self.assertEqual(result.stdout, b"")


if __name__ == "__main__":
    unittest.main()
