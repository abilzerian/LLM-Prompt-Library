#!/usr/bin/env python3
"""Build prompt indexes and update README counts.

Run from repo root:

```
python scripts/build_index.py
```
"""

from __future__ import annotations

import pathlib
import re
import textwrap
from typing import List
from urllib.parse import quote

PROMPTS_DIR = pathlib.Path("prompts")
INDEX_FILE = PROMPTS_DIR / "INDEX.md"
README_FILE = pathlib.Path("README.md")

def extract_title(path: pathlib.Path) -> str:
    """Grab first non‑empty heading line or fallback to filename."""
    for line in path.read_text(encoding="utf‑8").splitlines():
        if m := re.match(r"#\s*(.+)", line):
            return m.group(1).strip()
    return path.stem.replace("_", " ")


def pretty_category(name: str) -> str:
    """Convert folder name to human-friendly label."""
    label = name.replace("_", " ").title()
    if label == "Writing Editing":
        return "Writing & Editing"
    return label


def make_link(path: pathlib.Path) -> str:
    rel_path = path.relative_to(PROMPTS_DIR).as_posix()
    url = quote(f"prompts/{rel_path}", safe="/")
    return f"[{extract_title(path)}]({url})"

def main() -> None:
    files = sorted(PROMPTS_DIR.rglob("*.md"))
    rows: List[str] = []
    categories: dict[str, List[pathlib.Path]] = {}
    for f in files:
        if f.name == "INDEX.md":
            continue
        rel = f.relative_to(PROMPTS_DIR)
        categories.setdefault(rel.parts[0], []).append(f)
        url = quote(rel.as_posix(), safe="/")
        rows.append(f"| [{rel.as_posix()}]({url}) | {extract_title(f)} |")

    header = textwrap.dedent(
        """\
        <!--- AUTO‑GENERATED: do not edit manually.  Run scripts/build_index.py -->
        # Prompt Index

        | Path | Title |
        |------|-------|
    """
    )
    INDEX_FILE.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"Generated {INDEX_FILE} with {len(rows)} entries")

    # README table update
    table_rows = [
        "| Category | Prompts | Example\u00a0links |",
        "| -------- | ------: | ------------- |",
    ]
    total = 0
    for cat in sorted(categories):
        count = len(categories[cat])
        total += count
        examples = " \u2022 ".join(
            make_link(p) for p in sorted(categories[cat])[:2]
        )
        table_rows.append(
            f"| {pretty_category(cat)} | **{count}** | {examples or '—'} |"
        )
    table_rows.append(f"| **Total** | **{total}** | — |")

    start = "<!-- AUTO‑GENERATED: updated by scripts/build_index.py – do **not** edit manually -->"
    end = "<!-- /AUTO‑GENERATED -->"
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.DOTALL)
    replacement = "\n".join([start] + table_rows + [end])
    readme = README_FILE.read_text(encoding="utf-8")
    new_readme = re.sub(pattern, replacement, readme)
    README_FILE.write_text(new_readme, encoding="utf-8")
    print("Updated README counts")

if __name__ == "__main__":
    main()
