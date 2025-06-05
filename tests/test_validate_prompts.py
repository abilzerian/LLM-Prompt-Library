from scripts.validate_prompts import PromptValidator

def test_validate_file_ok(tmp_path):
    file = tmp_path / "prompt.md"
    long_content = "# Title\n```\n" + "line " * 20 + "\n```\n"
    file.write_text(long_content)
    validator = PromptValidator(root_dir=str(tmp_path))
    assert validator._validate_file(str(file))


def test_validate_file_missing_title_strict(tmp_path):
    file = tmp_path / "prompt.md"
    file.write_text("No title here\n```\ncontent\n```\n")
    validator = PromptValidator(root_dir=str(tmp_path), strict=True)
    assert not validator._validate_file(str(file))
