"""Autonomous data-analysis agent baseline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class AnalysisObservation:
    tool_name: str
    summary: str
    numeric_evidence: float | int


def load_orders(project_dir: Path) -> pd.DataFrame:
    orders = pd.read_csv(project_dir / "data" / "orders.csv")
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["month"] = orders["order_date"].dt.to_period("M").astype(str)
    return orders


def plan_tool(question: str) -> str:
    text = question.lower()
    if any(term in text for term in ["shape", "quality", "dataset"]):
        return "dataset_profile"
    if any(term in text for term in ["segment", "most revenue", "generates"]):
        return "segment_revenue"
    if any(term in text for term in ["trend", "month"]):
        return "monthly_trend"
    if any(term in text for term in ["unusual", "jump", "anomal"]):
        return "anomaly_scan"
    if any(term in text for term in ["repeat", "retention", "customers"]):
        return "retention_proxy"
    return "dataset_profile"


def dataset_profile(orders: pd.DataFrame) -> AnalysisObservation:
    missing_values = int(orders.isna().sum().sum())
    summary = (
        f"The dataset has {len(orders)} orders, {orders['customer_id'].nunique()} customers, "
        f"{orders['segment'].nunique()} segments, and {missing_values} missing values."
    )
    return AnalysisObservation("dataset_profile", summary, missing_values)


def segment_revenue(orders: pd.DataFrame) -> AnalysisObservation:
    revenue = orders.groupby("segment")["order_value"].sum().sort_values(ascending=False)
    top_segment = revenue.index[0]
    top_revenue = int(revenue.iloc[0])
    summary = f"{top_segment} customers generate the most revenue with ${top_revenue:,} in orders."
    return AnalysisObservation("segment_revenue", summary, top_revenue)


def monthly_trend(orders: pd.DataFrame) -> AnalysisObservation:
    monthly = orders.groupby("month")["order_value"].sum().sort_index()
    first_month = int(monthly.iloc[0])
    last_month = int(monthly.iloc[-1])
    change = last_month - first_month
    direction = "increased" if change >= 0 else "decreased"
    summary = f"Monthly revenue {direction} from ${first_month:,} to ${last_month:,}, a change of ${change:,}."
    return AnalysisObservation("monthly_trend", summary, change)


def anomaly_scan(orders: pd.DataFrame) -> AnalysisObservation:
    monthly = orders.groupby("month")["order_value"].sum().sort_index()
    jumps = monthly.diff().fillna(0)
    anomaly_month = jumps.abs().idxmax()
    anomaly_value = int(jumps.loc[anomaly_month])
    summary = f"The largest month-over-month movement is ${anomaly_value:,} in {anomaly_month}."
    return AnalysisObservation("anomaly_scan", summary, abs(anomaly_value))


def retention_proxy(orders: pd.DataFrame) -> AnalysisObservation:
    repeat_customers = orders.groupby("customer_id").size()
    repeat_count = int((repeat_customers > 1).sum())
    repeat_rate = repeat_count / orders["customer_id"].nunique()
    summary = f"{repeat_count} customers ordered more than once, a repeat-customer proxy of {repeat_rate:.1%}."
    return AnalysisObservation("retention_proxy", summary, repeat_rate)


TOOLS = {
    "dataset_profile": dataset_profile,
    "segment_revenue": segment_revenue,
    "monthly_trend": monthly_trend,
    "anomaly_scan": anomaly_scan,
    "retention_proxy": retention_proxy,
}


def run_data_analysis_agent(project_dir: Path) -> pd.DataFrame:
    orders = load_orders(project_dir)
    questions = pd.read_csv(project_dir / "data" / "analysis_questions.csv")
    rows = []

    for item in questions.to_dict(orient="records"):
        selected_tool = plan_tool(item["question"])
        observation = TOOLS[selected_tool](orders)
        answer = f"Plan: select `{selected_tool}`. Observation: {observation.summary}"
        rows.append(
            {
                "question_id": item["question_id"],
                "question": item["question"],
                "selected_tool": selected_tool,
                "expected_tool": item["expected_tool"],
                "observation": observation.summary,
                "numeric_evidence": observation.numeric_evidence,
                "answer": answer,
                "tool_match": selected_tool == item["expected_tool"],
                "has_numeric_evidence": pd.notna(observation.numeric_evidence),
                "trace_complete": bool(answer and observation.summary),
            }
        )

    trace = pd.DataFrame(rows)
    output_dir = project_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    trace.to_csv(output_dir / "data_analysis_agent_trace.csv", index=False)
    return trace