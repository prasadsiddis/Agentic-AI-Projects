from pathlib import Path

from src.agentic_ai.data_analysis_agent import run_data_analysis_agent


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent
    trace = run_data_analysis_agent(repo_root / "03-autonomous-data-analysis-agent")
    print(trace[["question_id", "selected_tool", "tool_match", "observation"]].to_string(index=False))