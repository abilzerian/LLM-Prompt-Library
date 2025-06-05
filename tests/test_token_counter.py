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


def test_count_file_tokens_fallback_encoding(tmp_path):
    file = tmp_path / "latin1.md"
    file.write_bytes(b"caf\xe9 content")
    tc = TokenCounter(tokenizer="other")
    assert tc.count_file_tokens(str(file)) == 2
