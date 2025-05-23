# GitAgent-Lite

> A ReAct-based autonomous agent that recommends the best GitHub tools for your task using OpenAI function calling.

---

## What is GitAgent-Lite?

GitAgent-Lite is a single-agent system that uses the **ReAct pattern** and **OpenAI function calling** to help developers discover high-quality GitHub tools tailored to their needs. Just describe your goal (e.g., _"extract text from PDFs"_) and the agent autonomously:

1. Understands your intent.
2. Calls relevant tools (functions) like GitHub search.
3. Analyzes results.
4. Recommends the most suitable project.

---

## Features

-  ReAct pattern-based structured reasoning.
-  Autonomous function calling with OpenAI GPT-4.
-  Real-time GitHub search integration.
-  Selects the best repo based on stars, activity, and relevance.
-  CLI-first experience.

---

##  Getting Started
---
```
.
├── main.py                # CLI entrypoint
├── agent.py               # ReAct agent logic using OpenAI
├── functions.py           # Tool function implementations (e.g., GitHub search)
├── prompts/
│   └── react_prompt.py    # ReAct prompt template
├── requirements.txt       # Python dependencies
└── README.md           

```
---