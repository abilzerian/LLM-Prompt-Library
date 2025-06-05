import pathlib

# Ignore example scripts that require heavy dependencies
ROOT = pathlib.Path(__file__).resolve().parent.parent
collect_ignore = [
    str(ROOT / "scripts" / "financial_metacognition" / "examples" / "demo_financial_metacognition.py"),
]
