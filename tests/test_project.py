from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from memoryforge.project import PROJECT_CONFIG, PROJECT_DIRS, create_project


class ProjectTests(unittest.TestCase):
    def test_create_project_creates_artifact_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = create_project(Path(tmp) / "project")

            self.assertTrue((project.root / PROJECT_CONFIG).is_file())
            for relative_dir in PROJECT_DIRS:
                self.assertTrue((project.root / relative_dir).is_dir(), relative_dir)

    def test_create_project_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            first = create_project(root)
            first.config_path.write_text("custom = true\n", encoding="utf-8")

            second = create_project(root)

            self.assertEqual(first.root, second.root)
            self.assertEqual(second.config_path.read_text(encoding="utf-8"), "custom = true\n")


if __name__ == "__main__":
    unittest.main()
