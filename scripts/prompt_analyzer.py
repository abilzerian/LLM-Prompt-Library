import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import llm_prompt_library.prompt_analyzer as _pa

_pa.NLTK_AVAILABLE = False

PromptAnalyzer = _pa.PromptAnalyzer
main = _pa.main

__all__ = ["PromptAnalyzer", "main"]


def __getattr__(name):
    if name == "NLTK_AVAILABLE":
        return _pa.NLTK_AVAILABLE
    raise AttributeError(name)


def __setattr__(name, value):
    if name == "NLTK_AVAILABLE":
        _pa.NLTK_AVAILABLE = value
    else:
        globals()[name] = value


if __name__ == "__main__":
    main()
