from pathlib import Path

from src.agentic_ai.code_review_agent import run_code_review_agent


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent
    trace = run_code_review_agent(repo_root / "04-agentic-code-review-debugger")
    print(trace[["case_id", "predicted_issue", "predicted_severity", "issue_match"]].to_string(index=False))