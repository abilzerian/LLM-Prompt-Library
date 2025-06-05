import os, textwrap

purpose_map = {
    "finance/10-KAnalyzer.md": "Summarize and analyze SEC 10-K filings.",
    "finance/venturecapitalist.md": "Perform investor-style diligence on a startup.",
    "medical/Cognitive Bias Assessment Tool.md": "Detect cognitive biases and propaganda in text.",
    "miscellaneous/ChatAGI.md": "Talk with ChatAGI, an unrestricted AGI persona.",
    "miscellaneous/Code Anything Now.md": "Role-play CAN, a limitless coding assistant.",
    "miscellaneous/Custom Instructions.md": "Apply custom tone and formatting preferences.",
    "miscellaneous/MultiverseGPT.md": "Combine multiple answers into a single best response.",
    "miscellaneous/antikythera.md": "Use the ANTIKYTHERA virtual persona script.",
    "miscellaneous/bitmap.md": "Output 16x16 bitmap images using text.",
    "miscellaneous/graphing.md": "Generate charts using JavaScript and image links.",
    "miscellaneous/textadventure.md": "Play an interactive post-apocalyptic text adventure.",
    "programming/AWS Architect.md": "Plan a secure, scalable AWS infrastructure.",
    "programming/Azure Architect.md": "Design a secure, scalable Azure deployment.",
    "programming/Code_Explainer.md": "Explain source code in plain English.",
    "programming/Copilot.md": "Offer programming solutions and strategy.",
    "programming/Data_Conversion_Specialist.md": "Convert data between JSON, CSV, and other formats.",
    "programming/ExcelFormulas.md": "Create advanced Excel formulas with explanations.",
    "programming/HTML.md": "Provide guidelines for writing semantic HTML.",
    "programming/Jinja2_Code_Optimizer.md": "Iteratively optimize Jinja2 templates.",
    "programming/LaTeX_specialist.md": "Fix and craft LaTeX documents.",
    "programming/OnePageWebsite.md": "Build a complete one-page website from requirements.",
    "programming/Python.md": "Guide best practices for Python programming.",
    "programming/PythonBugFixer.md": "Find and fix bugs in Python code.",
    "programming/Scientific Data Visualizer.md": "Visualize scientific data with dashboards.",
    "programming/UnstructuredText_to_JSON.md": "Transform unstructured text into JSON format.",
    "programming/Wolfram.md": "Write efficient Wolfram Language code.",
    "programming/commit messages.md": "Draft concise commit messages.",
    "programming/cursor_IDE_prompt.md": "Assist coding as the Cursor IDE persona.",
    "prompt_generation/CoT_Probe_o3.md": "Generate chain-of-thought reasoning probes.",
    "prompt_generation/DALL-E.md": "Craft short prompts for DALL-E image generation.",
    "prompt_generation/Midjourney.md": "Create weighted prompts for Midjourney images.",
    "prompt_generation/Prompt Creator.md": "Iteratively refine prompts with the user.",
    "prompt_generation/PromptScript.md": "Use PromptScript syntax to chain tasks.",
    "prompt_generation/PromptScriptEngineer.md": "Teach and apply the PromptScript method.",
    "prompt_generation/ScriptingTemplate.md": "Use the MNEMOSYNE scripting template persona.",
    "writing_editing/editing_revision/Preserve Technical Terminology.md": "Explain technical text in simpler language.",
    "writing_editing/editing_revision/Proofread.md": "Proofread text in a poetic style.",
    "writing_editing/editing_revision/Rewrite.md": "Rewrite text without changing length or structure.",
    "writing_editing/editing_revision/formatting.md": "Showcase advanced Markdown formatting.",
    "writing_editing/educational/Teach.md": "Tutor the user through practice sessions.",
    "writing_editing/educational/Thought Stream Transcription.md": "Clean and summarize a rough thought transcript.",
    "writing_editing/extraction_summarization/Action Items.md": "Extract actionable items aimed at the reader.",
    "writing_editing/extraction_summarization/Book Summary.md": "Summarize a book with detailed bullet points.",
    "writing_editing/extraction_summarization/Comprehensive Analysis.md": "Produce an in-depth commentary on an article.",
    "writing_editing/extraction_summarization/Non-Fiction Analysis.md": "Analyze a non-fiction article thoroughly.",
    "writing_editing/extraction_summarization/NotesGPT.md": "Create concise notes from text.",
    "writing_editing/extraction_summarization/Poem Analysis.md": "Write a detailed analysis of a poem.",
    "writing_editing/extraction_summarization/Short Summary.md": "Produce brief bullet-point summaries.",
    "writing_editing/verification/Accuracy Confirmation.md": "Highlight factual inaccuracies without fixes."
}

for rel_path, purpose in purpose_map.items():
    path = os.path.join('prompts', rel_path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if '## Purpose' in content:
        continue
    lines = content.splitlines()
    title = lines[0]
    rest = '\n'.join(lines[1:]).lstrip()
    new_content = f"{title}\n\n## Purpose\n{purpose}\n\n## Instructions\n{rest}"
    if not new_content.endswith('\n'):
        new_content += '\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
