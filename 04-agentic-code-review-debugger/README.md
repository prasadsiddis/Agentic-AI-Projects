# Agentic Code Review and Debugging Assistant

This project implements a code-review agent that reads small Python cases, inspects failing-test context, identifies likely defects, proposes fixes, and exports an evaluation trace.

## Problem

Developers often need help turning a failing test or suspicious function into a clear bug diagnosis. A useful debugging agent should inspect code, connect symptoms to root causes, suggest a safe patch strategy, and label risk.

## Agent Workflow

1. Load code review cases from `data/review_cases.json`.
2. Plan the review steps from the test failure and code snippet.
3. Run deterministic inspection rules.
4. Map the finding to severity and patch guidance.
5. Evaluate the predicted issue against the expected issue.
6. Export `outputs/code_review_agent_trace.csv`.

## Review Capabilities

- Mutable default argument detection
- Division-by-zero risk detection
- Off-by-one loop boundary detection
- Hard-coded secret detection
- Test-failure-aware explanation generation

## Run

```bash
python run_code_review_agent.py
```

## Why This Is Agentic

The project models a practical software-engineering agent loop: plan, inspect, reason over symptoms, produce a patch recommendation, and evaluate the result.