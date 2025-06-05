# Agents Guide for LLM-Prompt-Library

> This internal handbook is written for **autonomous AI agents** that contribute to the repository. Follow it exactly: the human will review every commit, and CI will reject non-conforming changes.

---

## 1  Mission & Scope

* Maintain a **high-quality, reusable prompt catalogue** and the Python tooling that supports it.
* Keep the project easy to audit. Every line of generated code or prose **must be explainable and traceable**.
* Prefer minimal, readable solutions over clever but opaque ones.

---

## 2  Repository Map

| Path | Purpose |
| ---- | ------- |
| `prompts/` | Markdown prompt templates, organised by category sub-folders. |
| `scripts/` | CLI utilities (validation, index builder, mixer, evolution, etc.). |
| `scripts/financial_metacognition/` | Finance-specific analysis helpers. |
| `docs/` | Additional long-form documentation. |
| `tests/` | Unit tests for Python helpers. |

---

## 3  Environment Setup

1. **Clone** & **install deps** (Python 3.9+):
   ```bash
   git clone https://github.com/abilzerian/LLM-Prompt-Library.git
   cd LLM-Prompt-Library
   python -m venv .venv && source .venv/bin/activate
   pip install -r scripts/requirements.txt
   ```
2. **Optional dev tools**:
   ```bash
   # linting & pre-commit hooks
   pip install ruff pre-commit && pre-commit install
   ```
3. **API keys** – set as env vars when required:
   * `OPENAI_API_KEY` for prompt-evolution or analyser scripts.
   * Other vendors as new features demand.

> **Tip:** In Codespaces/Gitpod simply run `./scripts/dev_bootstrap.sh` when it exists.

---

## 4  Daily Workflow (Agents)

1. **Create a feature branch**: `feat/<short-slug>`.
2. **Plan**: summarise intent in the commit description *before* generating code.
3. **Generate / edit files**:
   * Use small, iterative `edit_file` calls.
   * **Never** overwrite unchanged lines—use the `{{ ... }}` placeholder.
4. **Validate**:
   ```bash
   python scripts/validate_prompts.py           # structural checks
   python scripts/token_counter.py prompts/     # cost awareness
   ```
5. **Rebuild indices**:
   ```bash
   python scripts/build_index.py   # updates README & prompts/INDEX.md counts
   ```
6. **Run unit tests** *(when present)*: `pytest -q`.
7. **Commit** using conventional messages (e.g. `feat: add Stock Analyst prompt`).
8. **Open a Pull Request**; the CI pipeline enforces style + index freshness.

---

## 5  Prompt Authoring Rules

1. **File location**: `prompts/<category>/<Name>.md` (spaces allowed, keep Title Case).
2. **Front matter** *(optional)*: YAML header for meta-data (`tags`, `model`, etc.).
3. **Content sections** (recommended order):
   1. `## Purpose`
   2. `## Instructions`
   3. Examples / few-shots (`### Example 1`, `### Example 2`, …)
4. **Token budget**: aim < 700 tokens raw. Use the token counter.
5. **Style**:
   * Use **second-person** when addressing the model ("You are …").
   * Keep sentences short & imperative.
   * Preserve any existing DSL (`#BEGIN` / `#END`, bullets, tables).
6. **Cross-links**: reference related prompts with relative links.
7. **Validation**: file **must** pass `scripts/validate_prompts.py` before commit.

---

## 6  Python Scripts Cheat-Sheet

| Script | What it does |
| ------ | ------------ |
| `build_index.py` | Regenerates the prompt catalogue & README counts. |
| `validate_prompts.py` | Structural + lint checks on every prompt file. |
| `token_counter.py` | Prints token/char counts per prompt. |
| `prompt_mixer.py` | Combines multiple prompts into variants. |
| `prompt_analyzer.py` | LLM-powered quality report + suggestions. |
| `prompt_evolution.py` | Self-improvement loop for prompts. |
| `mixed_prompts/` | Output folder for mixer/evolution runs. |

> **Run `python <script> -h` for CLI options.**

---

## 7  AI Assistant Best Practices

* **Craft precise prompts from the given User Input** – break tasks into atomic steps, specify desired style.
* **Provide context** – open relevant files; mention function names in chat.
* **Review every suggestion** – check logic, security, licences.
* **Iterate** – if output is off, rephrase or supply examples.
* **Keep feedback loops tight** – commit small, run tests often.

---

## 8  Example Agent Sessions

### 8.1  Add a new prompt
```
USER  ▸ Create Stock Analyst prompt (category: finance). Use existing Finance style.
AI    ▸ writes `prompts/finance/Stock Analyst.md`, runs validator, updates index.
```

### 8.2  Refactor a script
```
USER  ▸ optimise scripts/token_counter.py
AI    ▸ edits file, adds unit test `tests/test_token_counter.py`, runs pytest.
```

### 8.3  Bulk token audit
```
USER  ▸ list prompts > 800 tokens
AI    ▸ runs token_counter, outputs markdown table with offenders.
```

---

## 9  CI & Pre-commit

* **ruff** – style & import sorting.
* **markdown-lint** – docs formatting.
* **pytest** – future unit tests.
* **build_index** – README & catalogue freshness.

CI runs on every PR; identical checks are available locally via:
```bash
pre-commit run --all-files
```

---

## 10  FAQ

**Q:** *Where should temporary or experimental prompts live?*

A: In `prompts/_sandbox/` which is excluded from the index.

**Q:** *Can an agent install a new Python dependency?*

A: Only after confirming no stdlib alternative exists and adding a pinned version to `scripts/requirements.txt`.

**Q:** *How do I update the live demo site?*

A: The GitHub Pages site auto-builds from `main` after `build_index.py` updates the static catalogue. No manual action needed.

---

You are now ready. Build responsibly ✨
