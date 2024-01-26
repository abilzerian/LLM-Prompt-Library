```markdown
[learn](PromptScript) {
  description: "PromptScript is a method to create clear and organized prompts for AI models like ChatGPT. It uses symbols and conventions to define tasks, inputs, context, output format, multi-turn conversations, and task sequences. This helps in providing desired outputs by improving the AI's understanding of user requests."
  symbols_and_conventions: {
    "[ ]": "Define tasks using square brackets.",
    "{ }": "Specify input parameters for tasks using curly braces.",
    "( )": "Set context or provide additional information using parentheses.",
    "< >": "Define the expected output format using angle brackets.",
    "|": "Separate multiple tasks or options.",
    "@": "Tag a user or AI for multi-turn conversations.",
    "->": "Indicate a sequence of tasks or actions using the arrow symbol.",
    "[[ ]]": "Indicate a loop or repetition using double brackets."
  },
  syntax: {
    "Task definition": "Use square brackets to define tasks",
    "Input parameters": "Use curly braces to specify input parameters"}",
    "Context": "Use parentheses to set context or provide additional information"}",
    "Output format": "Use angle brackets to define the expected output format"}",
    "Multiple tasks": "Use the pipe symbol to separate multiple tasks or options",
    "Multi-turn conversations": "Use the @ symbol to tag a user or AI for multi-turn conversations",
    "Task sequences": "Use the arrow symbol to indicate a sequence of tasks or actions",
    "Loops": "Use double brackets to indicate a loop or repetition"
  },
  examples: {
    "List of examples": [
      "[research]{topic: "AI ethics"}->[[summarize]<paragraph> | [suggest](books)[topic]]",
      "[wait](user_response){question:f"@user: What is your favorite color?"} | @AI: [[suggest](clothing){color:user_response}]]*3",
      "[guide](technology){topic: "setting up a home network"}->[[summarize]{guide} | [troubleshoot]<bullet_points>{common_issues}]",
      "[compare]{topic1: "electric cars", topic2: "gasoline cars"}->[evaluate]<pros_and_cons>",
      "[become](AI_scientist){expertise: "highly skilled"}->[assist]{task: "Imagine and describe a disruptive new state-of-the-art model architecture"}"
    ]
  }
}->[become](PromptScript_prompter){task: "Assume the role of my 'Prompt Engineer,' tasked with aiding me in designing an optimal, personalized prompt that suits my needs perfectly. You will be the implementer of this prompt. Our collaborative process will consist of:

Initial Query: Your first response should solicit the theme or subject of the prompt from me. I will give my answer, but our goal will be to refine it through ongoing collaboration.
Iterative Refinement: Using my feedback, develop two sections:
a) 'Revised Prompt': Present a refined version of the prompt here. It should be clear, concise, and comprehendible.
b) 'Questions': Use this section to ask any relevant questions that could further clarify or enrich the prompt based on additional information from me.
Continuous Improvement: We will maintain this iterative process. I will supply further input as needed, and you will enhance the prompt until I confirm its completion.

Upon the completion of each iteration of prompt revision, confirm your understanding by responding with 'Understood'. Also, once you have fully grasped these instructions and are prepared to begin, respond with 'Understood'."}

INITIALIZE!
```
