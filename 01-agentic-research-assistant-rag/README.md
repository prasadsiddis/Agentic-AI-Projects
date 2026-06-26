# Agentic Research Assistant with RAG

Notebook: `agentic_research_assistant_rag.ipynb`

## Overview

This project implements an end-to-end research assistant agent. The agent plans a research query, retrieves relevant source snippets, synthesizes an answer, checks citation coverage, and exports a trace for evaluation.

## Workflow

1. Classify the research question.
2. Decompose it into search tasks.
3. Retrieve candidate evidence from a local source corpus.
4. Synthesize a grounded answer.
5. Validate citation support.
6. Export the agent trace.

## Upgrade Path

- Replace lexical retrieval with embeddings.
- Add web search or academic paper search.
- Add LangGraph-style planner/retriever/synthesizer/checker nodes.
- Add LLM-based answer synthesis and citation verification.
