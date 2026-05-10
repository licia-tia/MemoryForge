from __future__ import annotations

import json
import unittest
from pathlib import Path


class SchemaTests(unittest.TestCase):
    def test_all_schema_files_are_valid_json_objects(self) -> None:
        schema_dir = Path(__file__).resolve().parents[1] / "docs" / "schemas"
        schemas = sorted(schema_dir.glob("*.schema.json"))

        self.assertGreaterEqual(len(schemas), 9)
        for path in schemas:
            with self.subTest(schema=path.name):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(payload["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(payload["type"], "object")


if __name__ == "__main__":
    unittest.main()
