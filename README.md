# rag-scratch

A from-scratch RAG pipeline for learning production AI/ML engineering patterns, built without high-level frameworks.
Stack

FastAPI, Sentence-Transformers, Qdrant client, Groq API, Langfuse, Vite + React

What it does

Ingests OpenStax PDFs and a SAT Math JSON dataset
Embeds and stores chunks in Qdrant using Sentence-Transformers directly
Exposes a /query endpoint for retrieval-augmented answers
Traces retrieval and LLM calls via Langfuse
Lite React UI for querying the API

Potential deployment stack

Backend: Render
Frontend: Vercel
Vector DB: Qdrant Cloud

