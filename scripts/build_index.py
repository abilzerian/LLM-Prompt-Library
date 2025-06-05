#!/usr/bin/env python3
"""
Builds prompts/INDEX.md with a table of all prompt files.
Run from repo root:  python scripts/build_index.py
"""

import pathlib
import re
import textwrap
from urllib.parse import quote

README_FILE = pathlib.Path("README.md")

PROMPTS_DIR = pathlib.Path("prompts")
INDEX_FILE  = PROMPTS_DIR / "INDEX.md"

CATEGORY_NAMES = {
    "writing_editing": "Writing\u00A0&\u00A0Editing",
    "programming": "Programming",
    "prompt_generation": "Prompt\u00A0Generation",
    "medical": "Medical",
    "finance": "Finance",
    "miscellaneous": "Miscellaneous",
}

def extract_title(path: pathlib.Path) -> str:
    """Grab first non‑empty heading line or fallback to filename."""
    for line in path.read_text(encoding="utf‑8").splitlines():
        if m := re.match(r"#\s*(.+)", line):
            return m.group(1).strip()
    return path.stem.replace("_", " ")


def build_catalogue_table() -> str:
    """Return markdown table rows summarizing prompt counts per category."""
    rows = []
    total = 0
    for category_path in sorted(PROMPTS_DIR.iterdir()):
        if not category_path.is_dir():
            continue
        files = sorted(category_path.rglob("*.md"))
        if not files:
            continue
        count = len(files)
        total += count
        title = CATEGORY_NAMES.get(
            category_path.name, category_path.name.replace("_", " ").title()
        )
        examples = []
        for f in files[:2]:
            rel = f.relative_to(PROMPTS_DIR).as_posix()
            url = quote(rel, safe="/")
            examples.append(f"[{extract_title(f)}](prompts/{url})")
        rows.append(f"| {title} | **{count}** | {' • '.join(examples)} |")
    rows.append(f"| **Total** | **{total}** | — |")
    return "\n".join(rows)


def update_readme(table_rows: str) -> None:
    text = README_FILE.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(<!-- AUTO\u2011GENERATED:.*?-->)(.*?)(<!-- /AUTO\u2011GENERATED -->)",
        re.S,
    )
    replacement = ("\\1\n| Category | Prompts | Example\u00A0links |\n"
                   "| -------- | ------: | ------------- |\n"
                   f"{table_rows}\n\\3")
    new_text = pattern.sub(replacement, text)
    README_FILE.write_text(new_text, encoding="utf-8")

def main() -> None:
    files = sorted(PROMPTS_DIR.rglob("*.md"))
    rows  = []
    for f in files:
        if f.name == "INDEX.md":
            continue
        rel_path = f.relative_to(PROMPTS_DIR).as_posix()
        url      = quote(rel_path, safe="/")     # “ ” → %20, “/” untouched
        rows.append(f"| [{rel_path}]({url}) | {extract_title(f)} |")

    header = textwrap.dedent("""\
        <!--- AUTO‑GENERATED: do not edit manually.  Run scripts/build_index.py -->
        # Prompt Index

        | Path | Title |
        |------|-------|
    """)
    INDEX_FILE.write_text(header + "\n".join(rows) + "\n", encoding="utf‑8")
    print(f"Generated {INDEX_FILE} with {len(rows)} entries")

    table = build_catalogue_table()
    update_readme(table)

if __name__ == "__main__":
    main()
