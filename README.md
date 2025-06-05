# LLM Prompt Library

[![GitHub stars](https://img.shields.io/github/stars/abilzerian/LLM-Prompt-Library?style=for-the-badge)](../../stargazers)
[![GitHub forks](https://img.shields.io/github/forks/abilzerian/LLM-Prompt-Library?style=for-the-badge)](../../network/members)
[![Issues](https://img.shields.io/github/issues/abilzerian/LLM-Prompt-Library?style=for-the-badge)](../../issues)
[![CI](https://img.shields.io/github/actions/workflow/status/abilzerian/LLM-Prompt-Library/ci.yml?branch=main&style=for-the-badge)](../../actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational?style=for-the-badge)](LICENSE)
[![Discord](https://img.shields.io/discord/1051259432199266374?style=for-the-badge&logo=discord)](https://discord.gg/chatgpt-prompt-engineering-1051259432199266374)
[![Twitter Follow](https://img.shields.io/twitter/follow/alexbilz?style=for-the-badge)](https://x.com/alexbilz)

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com/?lines=Prompt+Engineering+Library;18%2C000%2B+AI+Practitioners;Reusable+LLM+Templates;Multi‑Model+Support&font=Fira%20Code&center=true&width=520&height=45&duration=4000&pause=1000">
</div>

<p align="center">
  <a href="https://openai.com"><img src="https://img.shields.io/badge/GPT_o3-Optimized-brightgreen?style=flat-square" alt="GPT o3"></a>
  <a href="https://www.anthropic.com/claude"><img src="https://img.shields.io/badge/Claude_3-Opus-purple?style=flat-square" alt="Claude 3 Opus"></a>
  <a href="https://ai.meta.com/llama/"><img src="https://img.shields.io/badge/Llama_3-Enhanced-orange?style=flat-square" alt="Llama 3"></a>
  <a href="https://gemini.google.com"><img src="https://img.shields.io/badge/Gemini-Supported-red?style=flat-square" alt="Gemini"></a>
</p>

> **Battle‑tested prompt templates & dev‑scripts for every major LLM.**

---
## ⚡ Quick peek

* **Live demo** → <https://abilzerian.github.io/LLM-Prompt-Library/>  
  Zero-JS until you open the page; the prompt list is rendered client-side from `prompts/INDEX.md`.
  
---

## ✨ Prompt catalogue (live)

<!-- AUTO‑GENERATED: updated by scripts/build_index.py – do **not** edit manually -->
| Category | Prompts | Example links |
| -------- | ------: | ------------- |
| Writing & Editing | **15** | [Accuracy Confirmation](prompts/writing_editing/verification/Accuracy%20Confirmation.md) • [Proofread](prompts/writing_editing/editing_revision/Proofread.md) |
| Programming | **16** | [Azure Architect](prompts/programming/Azure%20Architect.md) • [UnstructuredText → JSON](prompts/programming/UnstructuredText_to_JSON.md) |
| Prompt Generation | **7** | [Prompt Creator](prompts/prompt_generation/Prompt%20Creator.md) • [DALL‑E](prompts/prompt_generation/DALL-E.md) |
| Medical | **3** | [Cognitive Bias Assessment Tool](prompts/medical/Cognitive%20Bias%20Assessment%20Tool.md) |
| Finance | **2** | [10‑K Analyzer](prompts/finance/10-KAnalyzer.md) • [Venture Capitalist](prompts/finance/venturecapitalist.md) |
| Miscellaneous | **8** | [TextAdventure](prompts/miscellaneous/textadventure) |
| **Total** | **51** | — |
<!-- /AUTO‑GENERATED -->

> 📖 Full list lives in [`prompts/INDEX.md`](prompts/INDEX.md) — rebuilt on every commit.

---

## 🚀 Quick start

```bash
git clone https://github.com/abilzerian/LLM-Prompt-Library.git
cd LLM-Prompt-Library

# helper scripts
pip install -r scripts/requirements.txt

# rebuild catalogue & README counts (CI & pre‑commit do this automatically)
python scripts/build_index.py
```
Need a demo or enterprise implementation? Contact <a href="https://x.com/alexbilz">Alex Bilzerian</a></sub>

⸻

The library includes several tools to help you work with prompts:

- **🔍 Prompt Validator** - Validates the format and contents of prompt files to ensure they meet our standards.
- **🔄 Prompt Mixer** - Create new prompts by mixing and matching elements from existing prompts.
- **🔢 Token Counter** - Analyze prompt files to count tokens and estimate API costs.
- **📊 Prompt Analyzer** - Evaluate the quality of prompts and get suggestions for improvements.
- **🔄 Prompt Evolution** - Automatically optimize prompts through iterative self-improvement cycles.
- **💰 Financial Metacognition** - Analyze AI interpretations of financial prompts to detect biases and limitations.

⸻

📊 Community & stats

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=abilzerian/LLM-Prompt-Library&type=Date&theme=dark">
    <img alt="Star history" src="https://api.star-history.com/svg?repos=abilzerian/LLM-Prompt-Library&type=Date">
  </picture>
</p>

⸻

📄 License

Distributed under the MIT License — see the full text in LICENSE.

<div align="right">
  <sub>© 2025 | Maintained by <a href="https://x.com/alexbilz">Alex Bilzerian</a></sub>
</div>
