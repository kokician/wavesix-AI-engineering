# AI-Powered Release Note Generator

This project uses OpenAI's GPT-4 and LangChain to automate the generation of structured release notes from GitHub repositories. It supports querying project issues using natural language and stores past notes for memory-based retrieval.

## Features

- **Query GitHub repos** using natural language (e.g., “Python visualization library”) and get back the most relevant repo.
-  **Generate release notes** from GitHub issues using GPT-4.
-  **Memory**: All generated notes are stored in a Chroma vector database with embeddings for retrieval and conversation history.
- **Query the memory**: Ask what’s been previously stored (e.g., “What was the issue with Python’s top library?”).

## Tech Stack

- [Python 3.10+](https://www.python.org/)
- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenAI GPT-4](https://platform.openai.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Dotenv](https://pypi.org/project/python-dotenv/)

## Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/release-note-ai.git
   cd release-note-ai
