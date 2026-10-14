# AI & GenAI Engineering Learning 

This repository is my hands-on learning space for building the skills to become
a **Generative AI Engineer** and, ultimately, a **Full-Stack AI Engineer**. It
collects small experiments, practice projects, and larger applications as I
learn how to build useful AI-powered products from data and models through to
APIs and user interfaces.

## Goals

- Build a strong foundation in Python, software engineering, and working with
  APIs.
- Understand how LLMs work in practice: prompting, structured outputs, model
  limitations, and evaluation.
- Learn embeddings, semantic search, vector stores, and retrieval-augmented
  generation (RAG).
- Build and connect AI features to reliable backend services and databases.
- Develop full-stack skills to create usable interfaces for AI applications.
- Learn to test, secure, deploy, monitor, and improve AI-powered applications.
- Turn what I learn into documented projects that demonstrate practical skills.

## Roadmap

This roadmap is a guide, not a strict schedule. I will add projects and update
progress as I build and learn.

### 1. Programming and development foundations

- Practice Python, modules, virtual environments, dependencies, and Git.
- Learn to read API documentation, handle errors, and write maintainable code.
- Build small scripts that solve clear problems.

### 2. LLM APIs and application basics

- Call hosted language models from Python.
- Learn prompt design, conversation messages, model parameters, and token usage.
- Validate model responses with schemas and handle invalid or incomplete output.
- Keep API keys in local environment variables; never commit secrets.

### 3. Embeddings and semantic search

- Generate embeddings for text and compare them with similarity measures.
- Explore chunking, metadata, and vector databases.
- Build search that retrieves relevant information by meaning, not just keywords.

### 4. Retrieval-augmented generation (RAG)

- Build an ingestion pipeline for documents and other knowledge sources.
- Retrieve relevant context and use it to ground model responses.
- Evaluate retrieval quality, answer relevance, and citations.
- Add safeguards for missing context, prompt injection, and sensitive data.

### 5. Backend and data systems

- Build APIs for AI features using a Python web framework.
- Work with databases, authentication, file uploads, background tasks, and
  validation.
- Design for latency, rate limits, retries, cost, and clear error handling.

### 6. Full-stack AI applications

- Build a frontend that makes AI features understandable and easy to use.
- Connect the frontend to backend APIs and show loading, streaming, and error
  states.
- Create complete applications such as document assistants, search tools, or
  workflow copilots.

### 7. Agents and tool use

- Learn function/tool calling and connect models to well-defined application
  actions.
- Build multi-step workflows with explicit limits, validation, and human
  approval where appropriate.
- Prefer predictable workflows over unnecessary autonomy.

### 8. Testing, evaluation, and deployment

- Write tests for application logic, API behavior, and AI workflow components.
- Create representative evaluation datasets and measure quality over time.
- Deploy an application and learn logging, monitoring, privacy, and operations.
- Document architecture, setup, limitations, and future improvements.

## Projects and practice

| Folder | Focus |
| --- | --- |
| [`day1/`](./day1/) | First Python and LLM practice |
| [`day2/`](./day2/) | Python environment and system practice |
| [`day3/`](./day3/) | Token and LLM API practice |
| [`day4/`](./day4/) | JSON and structured data with Pydantic |
| [`day8/`](./day8/) | Text embeddings and cosine similarity |
| [`day13/`](./day13/) | RAG practice |
| [`project/`](./project/) | AI resume-screening application |

These folders are snapshots of my learning: some are experiments, some are
projects in progress, and not every folder is a polished application yet.

## Working in this repository

Projects declare their dependencies in `pyproject.toml` files and use
[uv](https://docs.astral.sh/uv/) for Python environment and package management.
See each project's README for its setup and run instructions. For example, the
embedding project documents its steps in [`day8/README.md`](./day8/README.md).

Typical commands for a project in this workspace:

```powershell
uv sync --package day8
uv run --package day8 python day8\embading_rag.py
```

When a project needs another package, add it to that project rather than
installing it globally:

```powershell
uv add --project day8 <package-name>
```

## Learning approach

For each topic, I aim to:

1. Learn the core idea and build a small working example.
2. Test normal cases, edge cases, and failure behavior.
3. Expand the example into a useful application.
4. Record setup steps, design choices, limitations, and what I learned.
5. Improve the project based on testing and feedback.

## Security and responsible use

- Keep API keys and other credentials in local `.env` files or secret stores.
  Never commit them.
- Do not upload private documents or personal data without permission.
- Treat model output as fallible; validate it and keep people in control of
  important decisions.
- Be clear about what data an application sends to third-party model providers.

## Long-term outcome

The goal is to grow this repository from learning exercises into a portfolio of
reliable, documented AI applications that show end-to-end engineering: Python
and data handling, LLMs and RAG, backend APIs, frontend experiences, evaluation,
and deployment.
