# 🧠 Document Query Assistant — Backend

This is the **backend** for the Document Query Assistant — a system that allows users to upload documents (PDFs), processes and summarizes them, and enables question-answering using a retrieval-augmented generation (RAG) pipeline powered by OpenAI's GPT.

---

## 🚀 Features

- 📄 Upload and parse PDF documents
- 🧠 Automatic summarization of passages
- 🔍 Store embeddings for retrieval
- 💬 Ask questions and get answers based on relevant document content
- 🧾 Answer includes references and document/page sources
- 🖥️ interactive UI using Gradio

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/document-query-assistant.git
cd document-query-assistant/backend

---
```
### Run 

```
uvicorn main:app --reload or python main.py on terminal

---