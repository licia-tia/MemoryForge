from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from memoryforge.ingest import ingest_media


class IngestTests(unittest.TestCase):
    def test_ingest_writes_assets_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / "media"
            media.mkdir()
            (media / "photo.JPG").write_bytes(b"fake-jpeg")
            (media / "clip.mp4").write_bytes(b"fake-mp4")
            (media / "notes.txt").write_text("ignore me", encoding="utf-8")

            manifest = ingest_media(media, root / "project")

            self.assertEqual(manifest["counts"], {"total": 2, "photos": 1, "videos": 1})
            asset_types = {asset["media_type"] for asset in manifest["assets"]}
            self.assertEqual(asset_types, {"photo", "video"})
            self.assertTrue((root / "project" / "analysis" / "assets.json").is_file())

    def test_ingest_rejects_missing_media_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                ingest_media(Path(tmp) / "missing", Path(tmp) / "project")


if __name__ == "__main__":
    unittest.main()
