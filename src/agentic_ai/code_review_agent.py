"""Code review and debugging agent baseline."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class ReviewFinding:
    issue: str
    severity: str
    explanation: str
    patch_guidance: str


def load_cases(project_dir: Path) -> list[dict]:
    with (project_dir / "data" / "review_cases.json").open("r", encoding="utf-8") as file:
        return json.load(file)


def plan_review(case: dict) -> str:
    symptom = case["test_failure"].lower()
    if "security" in symptom or "credential" in symptom:
        return "inspect_failure > scan_secrets > classify_security_risk > propose_patch"
    if "zerodivision" in symptom:
        return "inspect_failure > scan_math_guards > classify_runtime_risk > propose_patch"
    return "inspect_failure > scan_code_patterns > classify_defect > propose_patch"


def inspect_code(code: str, symptom: str) -> ReviewFinding:
    lower_symptom = symptom.lower()

    if re.search(r"def\s+\w+\([^)]*=\[\]", code):
        return ReviewFinding(
            "mutable_default_argument",
            "medium",
            "A list default argument is reused across function calls, which explains state leaking between tests.",
            "Use None as the default, create a new list inside the function, then append the task.",
        )
    if "/ len(" in code or "zerodivisionerror" in lower_symptom:
        return ReviewFinding(
            "division_by_zero",
            "high",
            "The function divides by the length of an input collection without handling the empty case.",
            "Return 0, None, or raise a clear ValueError when the input list is empty before dividing.",
        )
    if "range(len(" in code and "- 1" in code:
        return ReviewFinding(
            "off_by_one_boundary",
            "medium",
            "The loop stops before the final index, so the last item is skipped.",
            "Iterate directly over items or use range(len(items)) when every element should be included.",
        )
    if re.search(r"(API_KEY|TOKEN|SECRET)\s*=\s*[\"']", code):
        return ReviewFinding(
            "hard_coded_secret",
            "critical",
            "A credential-like value is stored directly in source code.",
            "Move the secret to an environment variable or secret manager and rotate the exposed key.",
        )
    return ReviewFinding(
        "unknown",
        "low",
        "No deterministic rule matched the snippet.",
        "Add a targeted test case and inspect runtime behavior before patching.",
    )


def run_code_review_agent(project_dir: Path) -> pd.DataFrame:
    cases = load_cases(project_dir)
    rows = []

    for case in cases:
        plan = plan_review(case)
        finding = inspect_code(case["code"], case["test_failure"])
        final_review = (
            f"{finding.explanation} Recommended patch: {finding.patch_guidance} "
            f"Severity: {finding.severity}."
        )
        rows.append(
            {
                "case_id": case["case_id"],
                "title": case["title"],
                "plan": plan,
                "predicted_issue": finding.issue,
                "expected_issue": case["expected_issue"],
                "predicted_severity": finding.severity,
                "expected_severity": case["expected_severity"],
                "explanation": finding.explanation,
                "patch_guidance": finding.patch_guidance,
                "final_review": final_review,
                "issue_match": finding.issue == case["expected_issue"],
                "severity_match": finding.severity == case["expected_severity"],
                "has_patch_guidance": len(finding.patch_guidance) > 20,
                "risk_labeled": finding.severity in {"low", "medium", "high", "critical"},
                "trace_complete": bool(plan and final_review),
            }
        )

    trace = pd.DataFrame(rows)
    output_dir = project_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    trace.to_csv(output_dir / "code_review_agent_trace.csv", index=False)
    return trace