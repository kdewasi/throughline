"""Schemas for evaluation rule results and reports."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Severity = Literal["error", "warn"]


class RuleResult(BaseModel):
    """The outcome of evaluating one rule against a trajectory.

    Attributes
    ----------
    rule_id : str
        Stable identifier for the rule (e.g. "beat_count_in_range").
    severity : Severity
        "error" if a failure means the trajectory is invalid;
        "warn" if a failure is heuristic and merely suspicious.
    passed : bool
        Whether the rule's condition held.
    message : str
        One-sentence human-readable summary.
    details : dict
        Structured details for debugging (e.g. actual values, expected
        ranges). Empty dict if no details apply.
    """

    rule_id: str = Field(min_length=1, max_length=100)
    severity: Severity
    passed: bool
    message: str = Field(min_length=1, max_length=300)
    details: dict = Field(default_factory=dict)


class EvalReport(BaseModel):
    """The full evaluation result for one trajectory against all rules.

    A report `passed` if and only if all error-severity rules passed.
    Warn-severity failures do not affect overall pass/fail but are
    included in counts and surfaced in human-readable summaries.
    """

    trajectory_id: str = Field(min_length=1, max_length=100)
    prompt_version: str | None = Field(default=None, max_length=20)
    results: list[RuleResult]
    passed: bool
    error_count: int = Field(ge=0)
    warn_count: int = Field(ge=0)

    def summary_line(self) -> str:
        """One-line human-readable summary of the report."""
        status = "PASS" if self.passed else "FAIL"
        parts = [f"{status} {self.trajectory_id}"]
        if self.prompt_version:
            parts.append(f"(prompt {self.prompt_version})")
        if self.error_count:
            parts.append(f"errors: {self.error_count}")
        if self.warn_count:
            parts.append(f"warns: {self.warn_count}")
        return " — ".join(parts)