import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from llm_prompt_library.token_counter import TokenCounter, main

__all__ = ["TokenCounter", "main"]

if __name__ == "__main__":
    main()
