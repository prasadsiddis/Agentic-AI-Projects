# Autonomous Data Analysis Agent

This project implements a tool-using analyst agent that receives business questions, selects the right analysis tool, runs calculations on a real tabular dataset, and exports an evaluation trace.

## Problem

Analysts often receive broad questions such as "Which customer segment is growing fastest?" or "Are there anomalies in monthly revenue?" A useful agent should not answer directly from memory. It should plan, inspect the data, choose an analysis tool, compute evidence, and return a grounded answer.

## Agent Workflow

1. Parse the user question.
2. Select an analysis tool.
3. Execute the tool against `data/orders.csv`.
4. Synthesize an answer with computed metrics.
5. Compare the selected tool against the expected tool in `data/analysis_questions.csv`.
6. Export the full trace to `outputs/data_analysis_agent_trace.csv`.

## Tools

- `dataset_profile`: summarize rows, columns, date range, and missing values
- `segment_revenue`: compare revenue by customer segment
- `monthly_trend`: compute monthly revenue trends
- `anomaly_scan`: detect unusual monthly revenue movement
- `retention_proxy`: estimate repeat purchase behavior

## Run

```bash
python run_data_analysis_agent.py
```

## Why This Is Agentic

The project separates planning, tool routing, tool execution, answer synthesis, and evaluation. That makes the baseline simple enough to audit while still matching the structure of production agent systems.