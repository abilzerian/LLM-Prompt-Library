import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from llm_prompt_library.financial_metacognition.financial_metacognition import (
    analyze_financial_prompt,
    identify_financial_concepts,
    main,
)

__all__ = ["analyze_financial_prompt", "identify_financial_concepts", "main"]

if __name__ == "__main__":
    main()
