"""Positive contracts for the specification vault's canonical entry points."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "Automation Architecture"
CANONICAL = "https://github.com/MrWizard94-Compile/Agents-Constitution"


class GovernanceEntryTests(unittest.TestCase):
    def test_root_and_nested_entries_load_canonical_skill(self):
        for path in (ROOT / "AGENTS.md", VAULT / "AGENTS.md", VAULT / "CLAUDE.md"):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file(), "A usable entry must exist")
                text = path.read_text(encoding="utf-8")
                self.assertIn(CANONICAL, text)
                self.assertIn("wpai-constitution", text)
                self.assertRegex(text.lower(), r"\b(?:freeze|frozen)\b")

    def test_project_conventions_preserve_specification_boundary(self):
        text = (VAULT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("Obsidian specification vault, not a codebase", text)
        self.assertIn("one terse, single-purpose concept per note", text)
        self.assertIn("reciprocal links", text)
        self.assertIn("Leave `.obsidian/`", text)
        self.assertIn("not evidence that a running implementation exists", text)

    def test_orchestrator_routes_through_entries_and_director(self):
        text = (VAULT / "Orchestrator.md").read_text(encoding="utf-8")
        for required in ("[[AGENTS]]", "[[CLAUDE]]", "[[User]]", "accepted WPAI Constitution"):
            self.assertIn(required, text)
        self.assertNotIn("without exception", text)

    def test_changed_instruction_wiki_links_resolve_to_concept_notes(self):
        for name in ("AGENTS.md", "CLAUDE.md", "Orchestrator.md"):
            content = (VAULT / name).read_text(encoding="utf-8")
            for target in re.findall(r"\[\[([^\]|#]+)(?:[^\]]*)\]\]", content):
                with self.subTest(source=name, target=target):
                    self.assertTrue((VAULT / f"{target}.md").is_file(), target)


if __name__ == "__main__":
    unittest.main()
