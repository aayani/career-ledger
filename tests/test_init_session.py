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

    def test_creates_session_with_skill_scoped_checklists(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_WORK_ROOT) as temporary:
            repo = Path(temporary)
            skills = repo / ".agents" / "skills"
            career_source = skills / "career-ledger" / "references" / "checklist.md"
            career_source.parent.mkdir(parents=True)
            career_source.write_text("- [ ] Verify profile\n", encoding="utf-8")
            router_source = skills / "resume-router" / "references" / "checklist.md"
            router_source.parent.mkdir(parents=True)
            router_source.write_text("- [ ] Verify resume\n", encoding="utf-8")

            created = init_session(
                repo,
                datetime(2026, 11, 8, 12, 44, 6, tzinfo=timezone.utc),
            )

            self.assertEqual(created.name, "session-20261108T124406000000Z")
            self.assertTrue((created / "artifacts").is_dir())
            self.assertFalse((created / "checklist.md").exists())
            self.assertEqual(
                (created / "career-ledger" / "checklist.md").read_text(encoding="utf-8"),
                "- [ ] Verify profile\n",
            )
            self.assertEqual(
                (created / "resume-router" / "checklist.md").read_text(encoding="utf-8"),
                "- [ ] Verify resume\n",
            )


if __name__ == "__main__":
    unittest.main()
