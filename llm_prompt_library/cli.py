import argparse
import importlib
import sys

# Modules imported eagerly for backward compatibility with tests.
build_index = importlib.import_module("llm_prompt_library.build_index")
validate_prompts = importlib.import_module("llm_prompt_library.validate_prompts")
token_counter = importlib.import_module("llm_prompt_library.token_counter")
prompt_analyzer = importlib.import_module("llm_prompt_library.prompt_analyzer")
prompt_evolution = importlib.import_module("llm_prompt_library.prompt_evolution")
prompt_mixer = importlib.import_module("llm_prompt_library.prompt_mixer")


def _dispatch(func, args):
    """Run a module's main() with patched ``sys.argv``."""
    old_argv = sys.argv
    sys.argv = [sys.argv[0]] + args
    try:
        func()
    finally:
        sys.argv = old_argv


def main(argv=None):
    """Unified command line interface for library utilities."""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="llm-pl",
        description="LLM Prompt Library command line interface",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    commands = {
        "validate-prompts": validate_prompts,
        "build-index": build_index,
        "token-counter": token_counter,
        "prompt-analyzer": prompt_analyzer,
        "prompt-evolution": prompt_evolution,
        "prompt-mixer": prompt_mixer,
        "financial-metacognition": "llm_prompt_library.financial_metacognition.financial_metacognition",
    }

    for name in commands:
        subparsers.add_parser(name)

    args, remaining = parser.parse_known_args(argv)

    target = commands[args.command]
    if isinstance(target, str):
        module = importlib.import_module(target)
    else:
        module = target
    _dispatch(module.main, remaining)


if __name__ == "__main__":
    main()
