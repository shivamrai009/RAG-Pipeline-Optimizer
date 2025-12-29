# 🧪 RAG Pipeline Optimizer

> **Automated Experimentation & Evaluation for Retrieval-Augmented Generation**

Every company uses RAG (Retrieval-Augmented Generation), but almost no one knows *which* configuration works best for their specific data. This tool solves that by running parallel experiments with different chunking strategies and using an "LLM-as-a-judge" to score the results accurately.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![Status](https://img.shields.io/badge/Status-Active-success)

## 🚀 The Problem
- **Guesswork:** Developers often pick `chunk_size=1024` or `overlap=200` arbitrarily.
- **Opacity:** It's hard to tell if a RAG pipeline fails because of bad retrieval or bad generation.
- **Cost:** Running manual tests is slow and expensive.

## 🛠️ The Solution
The **RAG Pipeline Optimizer** is an end-to-end MLOps tool that:
1.  **Ingests Data:** Accepts PDF documents (e.g., HR policies, technical manuals).
2.  **Runs Parallel Experiments:** Automatically tests 3 distinct RAG strategies:
    - *Quick Glance:* Small chunks (512 tokens) for speed.
    - *Deep Dive:* Large chunks (1024 tokens) for context.
    - *Precise Snippet:* Micro chunks (256 tokens) for specificity.
3.  **Auto-Evaluates:** Uses **Llama-3.3 (70B)** as an impartial judge to score answers on "Relevance" and "Accuracy."
4.  **Visualizes Results:** Provides a Streamlit dashboard to compare performance metrics.

---

## 🏗️ Architecture

The project is built as a microservices architecture using Docker.

- **Frontend:** Streamlit (UI for uploading files and visualizing data).
- **Backend:** FastAPI (Orchestrates the RAG pipelines).
- **LLM Engine:** Groq API (Running Llama-3.1-8b for generation & Llama-3.3-70b for judging).
- **Vector Store:** ChromaDB (Ephemeral local storage for experiments).
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2` (Local CPU inference).

---
<img width="1894" height="933" alt="Image" src="https://github.com/user-attachments/assets/f70a3661-ede5-4c92-bd3e-cddcd35afca9" />

## 📂 Project Structure

```text
rag-optimizer/
├── backend/
│   ├── main.py            # FastAPI Entry Point
│   ├── pipelines.py       # RAG Strategy Logic (LangChain)
│   ├── evaluator.py       # LLM-as-a-Judge Logic
│   └── Dockerfile         # Backend Container Config
├── frontend/
│   ├── app.py             # Streamlit Dashboard
│   └── Dockerfile         # Frontend Container Config
├── requirements.txt       # Dependencies
└── README.md
<img width="1894" height="933" alt="Image" src="https://github.com/user-attachments/assets/f70a3661-ede5-4c92-bd3e-cddcd35afca9" />
