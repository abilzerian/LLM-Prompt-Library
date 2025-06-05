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
| Finance | **2** | [10-K Analyzer](prompts/finance/10-KAnalyzer.md) • [Act as a venture capitalist](prompts/finance/venturecapitalist.md) |
| Medical | **1** | [Cognitive Bias Assessment Tool](prompts/medical/Cognitive%20Bias%20Assessment%20Tool.md) |
| Miscellaneous | **8** | [ChatAGI](prompts/miscellaneous/ChatAGI.md) • [Code Anything Now](prompts/miscellaneous/Code%20Anything%20Now.md) |
| Programming | **16** | [AWS Architect](prompts/programming/AWS%20Architect.md) • [Azure Architect](prompts/programming/Azure%20Architect.md) |
| Prompt Generation | **7** | [CoT_Probe_o3](prompts/prompt_generation/CoT_Probe_o3.md) • [DALL-E](prompts/prompt_generation/DALL-E.md) |
| Writing & Editing | **14** | [Preserve Technical Terminology](prompts/writing_editing/editing_revision/Preserve%20Technical%20Terminology.md) • [Proofread](prompts/writing_editing/editing_revision/Proofread.md) |
| **Total** | **48** | — |
<!-- /AUTO‑GENERATED -->

> 📖 Full list lives in [`prompts/INDEX.md`](prompts/INDEX.md) — rebuilt on every commit.

---

## 🚀 Quick start

```bash
git clone https://github.com/abilzerian/LLM-Prompt-Library.git
cd LLM-Prompt-Library

# helper scripts
pip install -r scripts/requirements.txt

# install hook to auto-update the prompt catalogue
pip install pre-commit
pre-commit install

# manual rebuild (usually handled by pre‑commit/CI)
python scripts/build_index.py
```
<sub>Need a demo or enterprise implementation? Contact <a href="https://x.com/alexbilz">Alex Bilzerian</a></sub>

⸻

The library includes several tools to help you work with prompts:

- **🔍 Prompt Validator** - Validates the format and contents of prompt files to ensure they meet our standards.
- **🔄 Prompt Mixer** - Create new prompts by mixing and matching elements from existing prompts.
- **🔢 Token Counter** - Analyze prompt files to count tokens and estimate API costs.
- **📊 Prompt Analyzer** - Evaluate the quality of prompts and get suggestions for improvements.
- **🔄 Prompt Evolution** - Automatically optimize prompts through iterative self-improvement cycles.
- **💰 Financial Metacognition** - Analyze AI interpretations of financial prompts to detect biases and limitations.
- **🛡️ Cognitive Security** - Scan text for manipulative language and other risky wording.

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
