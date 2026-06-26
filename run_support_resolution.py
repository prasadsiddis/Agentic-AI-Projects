from pathlib import Path

from src.agentic_ai.support_resolution import run_support_agents


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent
    trace = run_support_agents(repo_root / "02-multi-agent-support-resolution")
    print(trace.to_string(index=False))