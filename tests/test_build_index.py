from pathlib import Path
from scripts.build_index import extract_title


def test_extract_title_heading(tmp_path: Path):
    file = tmp_path / "example.md"
    file.write_text("# Heading\nContent")
    assert extract_title(file) == "Heading"


def test_extract_title_fallback(tmp_path: Path):
    file = tmp_path / "Example_File.md"
    file.write_text("No heading here")
    assert extract_title(file) == "Example File"


def test_build_catalogue_table(monkeypatch, tmp_path: Path) -> None:
    from scripts import build_index

    prompts_dir = tmp_path / "prompts"
    finance = prompts_dir / "finance"
    finance.mkdir(parents=True)
    (finance / "one.md").write_text("# F1")
    (finance / "two.md").write_text("# F2")
    misc = prompts_dir / "misc"
    misc.mkdir()
    (misc / "m1.md").write_text("# M1")

    monkeypatch.setattr(build_index, "PROMPTS_DIR", prompts_dir)
    monkeypatch.setattr(build_index, "CATEGORY_NAMES", {"finance": "Finance", "misc": "Misc"})

    table = build_index.build_catalogue_table()
    assert "| Finance | **2** |" in table
    assert "| Misc | **1** |" in table
    assert "| **Total** | **3** |" in table


def test_update_readme(monkeypatch, tmp_path: Path) -> None:
    from scripts import build_index

    readme = tmp_path / "README.md"
    start = "<!-- AUTO\u2011GENERATED: placeholder -->"
    end = "<!-- /AUTO\u2011GENERATED -->"
    readme.write_text(f"Intro\n{start}\nold\n{end}\n")

    monkeypatch.setattr(build_index, "README_FILE", readme)
    build_index.update_readme("| Foo | Bar |")

    updated = readme.read_text()
    assert "| Category | Prompts | Example\u00A0links |" in updated
    assert "| Foo | Bar |" in updated
