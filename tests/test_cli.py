import pytest

import llm_prompt_library.cli as cli


def test_cli_dispatch(monkeypatch):
    called = {}

    def fake_main():
        called['run'] = True

    monkeypatch.setattr(cli, 'build_index', type('m', (), {'main': fake_main}))

    cli.main(['build-index'])

    assert called.get('run')


def test_cli_unknown_command(monkeypatch):
    with pytest.raises(SystemExit):
        cli.main([])
