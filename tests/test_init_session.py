import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.init_session import init_session


REPO_ROOT = Path(__file__).resolve().parent.parent
TEST_WORK_ROOT = REPO_ROOT / ".sessions" / ".test-work"


class InitSessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        TEST_WORK_ROOT.mkdir(parents=True, exist_ok=True)

    def test_creates_session_with_checklist(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_WORK_ROOT) as temporary:
            repo = Path(temporary)
            source = repo / ".agents" / "skills" / "career-ledger" / "references" / "checklist.md"
            source.parent.mkdir(parents=True)
            source.write_text("- [ ] Verify\n", encoding="utf-8")

            created = init_session(
                repo,
                datetime(2026, 11, 8, 12, 44, 6, tzinfo=timezone.utc),
            )

            self.assertEqual(created.name, "session-20261108T124406000000Z")
            self.assertTrue((created / "artifacts").is_dir())
            copied = created / "checklist.md"
            self.assertEqual(copied.read_text(encoding="utf-8"), "- [ ] Verify\n")


if __name__ == "__main__":
    unittest.main()
