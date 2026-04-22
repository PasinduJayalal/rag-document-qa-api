# RAG Document Q&A API

A lightweight Retrieval-Augmented Generation (RAG) application that allows users to upload text or PDF documents and ask questions based strictly on the uploaded context.

## Features
- Upload text or PDF documents
- Chunk and process document content
- Store embeddings in a lightweight vector database
- Retrieve relevant context for each question
- Generate answers using an LLM
- Return "I don't know" when the answer is not supported by the provided context

This project is a portfolio-ready backend application that demonstrates:
- REST API design
- document ingestion
- vector-based retrieval
- LLM integration
- Dockerization and deployment