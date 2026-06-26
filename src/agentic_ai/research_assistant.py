"""Agentic research assistant baseline."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from math import sqrt
from pathlib import Path

import pandas as pd


@dataclass
class ResearchState:
    question_id: str
    question: str
    expected_sources: list[str]
    plan: list[str] = field(default_factory=list)
    retrieved_sources: list[tuple[str, float]] = field(default_factory=list)
    answer: str = ""
    citations: list[str] = field(default_factory=list)
    checks: dict[str, float | bool] = field(default_factory=dict)


def tokenize(text: str) -> list[str]:
    return [token.strip(".,?!;:").lower() for token in str(text).split() if token.strip(".,?!;:")]


def cosine_score(query: str, document: str) -> float:
    query_counts = Counter(tokenize(query))
    document_counts = Counter(tokenize(document))
    numerator = sum(query_counts[token] * document_counts.get(token, 0) for token in query_counts)
    query_norm = sqrt(sum(value * value for value in query_counts.values()))
    document_norm = sqrt(sum(value * value for value in document_counts.values()))
    if query_norm == 0 or document_norm == 0:
        return 0.0
    return numerator / (query_norm * document_norm)


def plan_research(state: ResearchState) -> ResearchState:
    text = state.question.lower()
    state.plan = ["retrieve_evidence", "synthesize_answer", "check_citations"]
    if any(term in text for term in ["evaluate", "should", "when"]):
        state.plan.insert(1, "inspect_risk_or_quality")
    return state


def retrieve_sources(state: ResearchState, sources: pd.DataFrame, top_k: int = 2) -> ResearchState:
    scored = []
    for row in sources.itertuples():
        document = f"{row.title} {row.domain} {row.text}"
        scored.append((row.source_id, cosine_score(state.question, document)))
    state.retrieved_sources = sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]
    return state


def synthesize_answer(state: ResearchState, sources: pd.DataFrame) -> ResearchState:
    source_lookup = sources.set_index("source_id").to_dict(orient="index")
    top_ids = [source_id for source_id, _ in state.retrieved_sources]
    state.answer = " ".join(source_lookup[source_id]["text"] for source_id in top_ids)
    state.citations = top_ids
    return state


def check_citations(state: ResearchState) -> ResearchState:
    expected = set(state.expected_sources)
    cited = set(state.citations)
    state.checks = {
        "source_recall": len(expected & cited) / max(len(expected), 1),
        "has_citation": bool(cited),
        "trace_complete": bool(state.plan and state.retrieved_sources and state.answer and state.citations),
    }
    return state


def run_research_agent(project_dir: Path) -> pd.DataFrame:
    data_dir = project_dir / "data"
    output_dir = project_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    sources = pd.read_csv(data_dir / "sample_sources.csv")
    questions = pd.read_csv(data_dir / "sample_questions.csv")

    states = []
    for row in questions.itertuples():
        state = ResearchState(
            question_id=row.question_id,
            question=row.question,
            expected_sources=str(row.expected_sources).split(";"),
        )
        state = plan_research(state)
        state = retrieve_sources(state, sources)
        state = synthesize_answer(state, sources)
        state = check_citations(state)
        states.append(state)

    trace = pd.DataFrame(
        [
            {
                "question_id": state.question_id,
                "question": state.question,
                "plan": " > ".join(state.plan),
                "retrieved_sources": ";".join(source for source, _ in state.retrieved_sources),
                "citations": ";".join(state.citations),
                "answer": state.answer,
                **state.checks,
            }
            for state in states
        ]
    )
    trace.to_csv(output_dir / "research_agent_trace.csv", index=False)
    return trace
