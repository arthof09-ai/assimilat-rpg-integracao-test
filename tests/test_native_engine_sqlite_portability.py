"""SQLite portability regressions for original VLAB native CI (TEST only)."""
import sqlite3
import tempfile
import unittest
from pathlib import Path

from scripts.native_engine_ci import sqlite_content_fingerprint


class SqliteSemanticPortability(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="R237_SQL_TEST_")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def database(self, name, rows):
        path = self.root / name
        with sqlite3.connect(path) as db:
            db.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, payload TEXT, amount REAL, raw BLOB)")
            db.executemany("INSERT INTO events VALUES (?,?,?,?)", rows)
            db.commit()
        return path

    def test_reordered_inserts_same_semantics(self):
        rows = [(1, '{"a":2}', 1.5, b'\x00\xff'), (2, "hello", -2.0, b'bytes')]
        left = self.database("left.sqlite", rows)
        right = self.database("right.sqlite", list(reversed(rows)))
        self.assertEqual(sqlite_content_fingerprint(left), sqlite_content_fingerprint(right))

    def test_changed_value_detected(self):
        original = [(1, '{"a":2}', 1.5, b'\x00\xff')]
        left = self.database("left.sqlite", original)
        right = self.database("right.sqlite", [(1, '{"a":2}', 1.6, b'\x00\xff')])
        self.assertNotEqual(sqlite_content_fingerprint(left), sqlite_content_fingerprint(right))

    def test_mutated_schema_detected(self):
        left = self.database("left.sqlite", [(1, "x", 1.0, b"")])
        right = self.database("right.sqlite", [(1, "x", 1.0, b"")])
        with sqlite3.connect(right) as db:
            db.execute("ALTER TABLE events ADD COLUMN extra TEXT")
        self.assertNotEqual(sqlite_content_fingerprint(left), sqlite_content_fingerprint(right))

    def test_damaged_sqlite_rejected(self):
        path = self.root / "broken.sqlite"
        path.write_bytes(b"not a sqlite database")
        with self.assertRaises((sqlite3.DatabaseError, AssertionError)):
            sqlite_content_fingerprint(path)


if __name__ == "__main__":
    unittest.main()
