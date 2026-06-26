# Agentic AI Projects

End-to-end Agentic AI portfolio projects focused on tool use, planning, retrieval, evaluation, and multi-agent workflows.

These projects are designed to run without paid API keys by using transparent baseline agents. The structure is ready to upgrade later with LLM APIs, local open-weight models, LangGraph-style state machines, AutoGen-style multi-agent conversations, or CrewAI-style task crews.

## Projects

| # | Project | Focus |
|---|---|---|
| 01 | [Agentic Research Assistant with RAG](01-agentic-research-assistant-rag/README.md) | Query planning, retrieval, source-grounded synthesis, citation checking, and evaluation |
| 02 | [Multi-Agent Support Resolution System](02-multi-agent-support-resolution/README.md) | Ticket triage, tool routing, specialist agents, escalation decisions, and response quality checks |

## What This Repo Demonstrates

- Agent planning and task decomposition
- Tool selection and observation handling
- Retrieval-augmented reasoning
- Multi-agent role separation
- Safety and confidence checks
- Evaluation traces and reproducible experiment configs

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Each notebook uses small sample datasets under its project folder and exports trace files under `outputs/` when run.

## References

- LangGraph: https://langchain-ai.github.io/langgraph/
- Microsoft AutoGen: https://microsoft.github.io/autogen/
- CrewAI: https://docs.crewai.com/

## Python Source Code

Standalone Python implementations are available under `src/agentic_ai/`.

```bash
python run_research_assistant.py
python run_support_resolution.py
```

The scripts run the same baseline agent workflows as the notebooks and export trace CSV files under each project folder's ignored `outputs/` directory.
