from __future__ import annotations

import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from memoryforge.cli import main


class CliTests(unittest.TestCase):
    def test_init_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with redirect_stdout(StringIO()):
                exit_code = main(["init", str(Path(tmp) / "project")])

            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "project" / "memoryforge.toml").is_file())

    def test_reserved_command_returns_not_implemented(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with redirect_stderr(StringIO()):
                exit_code = main(["plan", "--project", str(Path(tmp) / "project")])

            self.assertEqual(exit_code, 2)


if __name__ == "__main__":
    unittest.main()
