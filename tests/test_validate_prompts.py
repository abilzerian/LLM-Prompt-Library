from scripts.validate_prompts import PromptValidator


def test_validate_prompts_detects_missing_title(tmp_path):
    bad_file = tmp_path / "bad.md"
    bad_file.write_text("Some text but no heading.")

    validator = PromptValidator(root_dir=str(tmp_path), strict=True)
    result = validator.validate_all()

    assert result is False


def test_validate_prompts_accepts_valid_file(tmp_path):
    good_file = tmp_path / "good.md"
    good_file.write_text("""# Title
```text
You are an assistant. Your task is to test the validator.
Make sure there is enough text to exceed fifty characters in total.
```
""")

    validator = PromptValidator(root_dir=str(tmp_path), strict=True)
    result = validator.validate_all()

    assert result is True

