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
