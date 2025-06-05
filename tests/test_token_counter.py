import os
import pytest
from scripts.token_counter import TokenCounter


def test_extract_content_strip_markdown():
    text = "# Title\nSome *bold* text\n- item"
    tc = TokenCounter(include_markdown=False)
    assert tc.extract_content(text) == "Some bold text"


def test_extract_content_keep_markdown():
    text = "# Title\nSome *bold* text\n- item"
    tc = TokenCounter(include_markdown=True)
    assert tc.extract_content(text) == text


def test_extract_content_remove_code_block():
    text = "# Title\n\n```python\nprint('hi')\n```\nAfter code"
    tc = TokenCounter(include_markdown=False, include_code_blocks=False)
    assert tc.extract_content(text) == "After code"


def test_count_tokens_fallback():
    tc = TokenCounter(tokenizer="other")
    assert tc.count_tokens("hello world") == 2


def test_count_file_tokens_no_code(tmp_path):
    file = tmp_path / "file.md"
    file.write_text("# Title\n```python\nprint('hi')\n```\nAfter")
    tc = TokenCounter(include_markdown=False, include_code_blocks=False)
    tokens = tc.count_file_tokens(str(file))
    assert tokens == tc.count_tokens("After")


def test_analyze_all_counts(tmp_path):
    prompts_dir = tmp_path / "prompts"
    cat = prompts_dir / "cat"
    cat.mkdir(parents=True)
    file = cat / "t.md"
    file.write_text("hello world")

    tc = TokenCounter(root_dir=str(prompts_dir), tokenizer="other")
    results = tc.analyze_all()

    expected_path = os.path.relpath(file, start=os.getcwd())
    assert results["total"]["files"] == 1
    assert results["total"]["tokens"] == 2
    assert results["by_category"]["cat"]["files"] == 1
    assert results["by_file"][expected_path] == 2
