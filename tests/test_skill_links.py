"""The fork's gate: the skill is markdown, so what can break is its wiring.

A relative link that no longer resolves sends the agent to a file that is not there, and it reads
the silence as "nothing to load". A SKILL.md without `name`/`description` frontmatter is not
discovered at all. Both arrive quietly with an edit or an upstream merge.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
DOCS = [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md")),
        *sorted((ROOT / "assets").rglob("*.md"))]


def test_every_relative_link_resolves():
    assert len(DOCS) > 5, "found almost no docs -- the glob is measuring nothing"
    broken, seen = [], 0
    for doc in DOCS:
        for target in LINK.findall(doc.read_text()):
            if "://" in target or target.startswith("mailto:"):
                continue
            seen += 1
            if not (doc.parent / target).exists():
                broken.append(f"{doc.relative_to(ROOT)} -> {target}")
    assert seen > 5, "found almost no relative links -- the pattern is measuring nothing"
    assert not broken, broken


def test_skill_frontmatter_names_and_describes_it():
    head = (ROOT / "SKILL.md").read_text().split("---")[1]
    assert re.search(r"^name: icm-architect$", head, re.M)
    assert re.search(r"^description: \S", head, re.M)


def test_hub_adaptation_is_routed_from_skill_md():
    """hub.md only works if SKILL.md sends the agent there before it acts on the defaults."""
    assert (ROOT / "references/hub.md").is_file()
    assert "references/hub.md" in (ROOT / "SKILL.md").read_text().split("## The invariants")[0]
