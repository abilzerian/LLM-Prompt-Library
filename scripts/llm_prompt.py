#!/usr/bin/env python3
"""Unified command-line interface for the LLM Prompt Library."""

import argparse
import importlib

COMMAND_MODULES = {
    "validate": "validate_prompts",
    "mix": "prompt_mixer",
    "count": "token_counter",
    "analyze": "prompt_analyzer",
    "evolve": "prompt_evolution",
    "financial-metacognition": "financial_metacognition.financial_metacognition",
}

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="llm-prompt",
        description="LLM Prompt Library command-line tools",
        usage="llm-prompt <command> [<args>]",
    )
    parser.add_argument("command", help="Subcommand to run", nargs="?")
    args, remaining = parser.parse_known_args(argv)

    if not args.command:
        parser.print_help()
        parser.exit()

    module_path = COMMAND_MODULES.get(args.command)
    if not module_path:
        parser.error(f"Unknown command: {args.command}")

    module = importlib.import_module(f"scripts.{module_path}")
    if hasattr(module, "main"):
        module.main(remaining)
    else:
        parser.error(f"Module {module_path} does not define a main() function")

if __name__ == "__main__":
    main()
