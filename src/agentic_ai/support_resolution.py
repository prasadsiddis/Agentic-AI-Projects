"""Multi-agent support resolution baseline."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def triage_agent(message: str, customer_tier: str) -> tuple[str, str]:
    text = message.lower()
    if any(term in text for term in ["refund", "damaged", "return"]):
        route = "refund_specialist"
    elif any(term in text for term in ["invoice", "billing", "renewal"]):
        route = "billing_specialist"
    else:
        route = "technical_specialist"

    risk = "high" if customer_tier == "enterprise" and any(term in text for term in ["blocked", "cancel", "outage"]) else "medium" if customer_tier == "enterprise" else "low"
    return route, risk


def select_tool(route: str, message: str, tools: dict[str, str]) -> tuple[str, str]:
    text = message.lower()
    if route == "refund_specialist":
        return "refund_policy", tools["refund_policy"]
    if route == "billing_specialist":
        return "billing_policy", tools["billing_policy"]
    if "outage" in text:
        return "outage_policy", tools["outage_policy"]
    return "api_key_help", tools["api_key_help"]


def specialist_response(route: str, observation: str) -> str:
    if route == "refund_specialist":
        return f"I can help with the damaged item. Policy found: {observation}"
    if route == "billing_specialist":
        return f"This billing issue needs account review. Policy found: {observation}"
    return f"Technical guidance: {observation}"


def policy_checker(route: str, risk_level: str, observation: str, draft_response: str) -> dict[str, bool]:
    return {
        "uses_tool_observation": observation in draft_response,
        "has_customer_safe_language": not any(
            term in draft_response.lower()
            for term in ["guarantee", "definitely refund immediately"]
        ),
        "needs_human_review": risk_level == "high" or route == "billing_specialist",
    }


def final_response(draft_response: str, escalate: bool) -> str:
    if escalate:
        return draft_response + " I am escalating this for human review because of account risk or complexity."
    return draft_response + " This can be handled through the standard support workflow."


def run_support_agents(project_dir: Path) -> pd.DataFrame:
    data_dir = project_dir / "data"
    output_dir = project_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    tickets = pd.DataFrame(json.loads((data_dir / "sample_tickets.json").read_text(encoding="utf-8")))
    tools = json.loads((data_dir / "tool_outputs.json").read_text(encoding="utf-8"))

    rows = []
    for ticket in tickets.itertuples():
        route, risk_level = triage_agent(ticket.message, ticket.customer_tier)
        tool_name, observation = select_tool(route, ticket.message, tools)
        draft = specialist_response(route, observation)
        checks = policy_checker(route, risk_level, observation, draft)
        escalate = checks["needs_human_review"]
        response = final_response(draft, escalate)
        rows.append(
            {
                "ticket_id": ticket.ticket_id,
                "customer_tier": ticket.customer_tier,
                "message": ticket.message,
                "route": route,
                "risk_level": risk_level,
                "tool_name": tool_name,
                "tool_observation": observation,
                "draft_response": draft,
                "escalate": escalate,
                "final_response": response,
                "route_match": route == ticket.expected_route,
                "escalation_match": escalate == ticket.expected_escalation,
                **checks,
            }
        )

    trace = pd.DataFrame(rows)
    trace.to_csv(output_dir / "support_agent_trace.csv", index=False)
    return trace
