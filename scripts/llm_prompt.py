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
        add_help=False,
    )
    parser.add_argument("command", nargs="?", help="Subcommand to run")
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")
    args, remaining = parser.parse_known_args(argv)

    if args.help or not args.command:
        parser.print_help()
        print("\nAvailable commands:", ", ".join(sorted(COMMAND_MODULES)))
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
