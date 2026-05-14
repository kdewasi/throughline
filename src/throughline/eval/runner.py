"""Orchestrator for running all evaluation rules against a trajectory."""

from __future__ import annotations

from throughline.eval.rules import ALL_RULES, Rule
from throughline.eval.schemas import EvalReport, RuleResult
from throughline.schemas import Trajectory


def evaluate_trajectory(
    trajectory: Trajectory,
    *,
    prompt_version: str | None = None,
    rules: list[Rule] | None = None,
) -> EvalReport:
    """Run all rules against a trajectory and assemble an EvalReport.

    Parameters
    ----------
    trajectory
        The Trajectory to evaluate.
    prompt_version
        Optional label for which prompt produced this trajectory. Used
        only for reporting; does not affect any rule's behavior.
    rules
        Override the default rule set. Useful for tests that want to
        exercise only a subset.

    Returns
    -------
    An EvalReport. `passed` is True iff every error-severity rule passed.
    Warn-severity failures do not affect `passed`.
    """
    rules_to_run = rules if rules is not None else ALL_RULES

    results: list[RuleResult] = []
    for rule in rules_to_run:
        try:
            result = rule(trajectory)
        except Exception as exc:  # noqa: BLE001 — we genuinely want any failure here
            result = RuleResult(
                rule_id=rule.__name__,
                severity="error",
                passed=False,
                message=f"Rule raised an exception: {type(exc).__name__}: {exc}",
                details={"exception_type": type(exc).__name__},
            )
        results.append(result)

    error_count = sum(
        1 for r in results if r.severity == "error" and not r.passed
    )
    warn_count = sum(
        1 for r in results if r.severity == "warn" and not r.passed
    )
    passed = error_count == 0

    return EvalReport(
        trajectory_id=trajectory.film_id,
        prompt_version=prompt_version,
        results=results,
        passed=passed,
        error_count=error_count,
        warn_count=warn_count,
    )