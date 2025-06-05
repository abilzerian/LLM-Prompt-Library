#!/usr/bin/env python3
"""Simple cognitive security analyzer."""
import argparse
import json
import os
import re
from typing import Dict, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config", "risk_terms.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    RISK_TERMS: Dict[str, List[str]] = json.load(f)


def analyze_text(text: str) -> Dict[str, int]:
    """Count occurrences of risk terms in text."""
    counts: Dict[str, int] = {}
    lower_text = text.lower()
    for category, terms in RISK_TERMS.items():
        count = 0
        for term in terms:
            # simple word boundary search
            if re.search(r"\b" + re.escape(term) + r"\b", lower_text):
                count += 1
        counts[category] = count
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze text for cognitive security risks")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Text to analyze")
    group.add_argument("--file", type=str, help="File containing text to analyze")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = args.text

    counts = analyze_text(text)
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
