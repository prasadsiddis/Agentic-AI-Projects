# Multi-Agent Support Resolution System

Notebook: `multi_agent_support_resolution.ipynb`

## Overview

This project implements a multi-agent support workflow. A triage agent classifies tickets, specialist agents propose actions, a policy checker validates the answer, and an escalation agent decides when human review is required.

## Workflow

1. Load support tickets and customer context.
2. Triage tickets by intent and risk.
3. Route to specialist agents.
4. Call simulated tools such as order lookup and policy search.
5. Draft a response.
6. Run safety and escalation checks.
7. Export the multi-agent trace.

## Upgrade Path

- Replace rule-based agents with LLM role prompts.
- Add real tools and function-calling schemas.
- Add human-in-the-loop review for low-confidence cases.
- Add automated regression tests for ticket outcomes.
