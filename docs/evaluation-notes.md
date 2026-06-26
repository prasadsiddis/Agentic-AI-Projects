# Evaluation Notes

Agentic AI systems need more than final-answer evaluation. This repository tracks intermediate behavior as well.

## Core Metrics

| Metric | Meaning |
|---|---|
| tool_coverage | Did the agent use the tools needed for the task? |
| unnecessary_tool_count | Did the agent call extra tools? |
| grounding_score | Is the final answer supported by retrieved evidence or tool observations? |
| escalation_accuracy | Did the system escalate cases that need human review? |
| trace_completeness | Are plan, action, observation, and final answer recorded? |

## Review Questions

- Did the agent decompose the task correctly?
- Were tools selected for defensible reasons?
- Did the system avoid unsupported claims?
- Did it escalate ambiguous or risky cases?
- Can a reviewer reproduce the decision trace?
