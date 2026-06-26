from pathlib import Path

from src.agentic_ai.research_assistant import run_research_agent


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent
    trace = run_research_agent(repo_root / "01-agentic-research-assistant-rag")
    print(trace.to_string(index=False))