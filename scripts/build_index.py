import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from llm_prompt_library.build_index import (
    main,
    extract_title,
    build_site_sections,
)

__all__ = ["main", "extract_title", "build_site_sections"]

if __name__ == "__main__":
    main()
