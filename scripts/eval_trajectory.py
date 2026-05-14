"""CLI: run the evaluation harness against one trajectory JSON file.

Usage:
    uv run python scripts/eval_trajectory.py <trajectory_file>

Example:
    uv run python scripts/eval_trajectory.py data/trajectories/dark_knight_v2.json

Prints a per-rule summary and exits 0 if all error-severity rules
passed, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from throughline.eval.runner import evaluate_trajectory
from throughline.schemas import Trajectory

_PROMPT_VERSION_PATTERN = re.compile(r"_v(\d+(?:\.\d+)?)\.json$")


def _infer_prompt_version(path: Path) -> str | None:
    """Pull the prompt version suffix from filenames like dark_knight_v2.json."""
    match = _PROMPT_VERSION_PATTERN.search(path.name)
    return f"v{match.group(1)}" if match else None


def main(trajectory_path: str) -> int:
    path = Path(trajectory_path)
    if not path.exists():
        print(f"ERROR: trajectory file not found: {path}", file=sys.stderr)
        return 1

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    trajectory = Trajectory.model_validate(data)
    prompt_version = _infer_prompt_version(path)

    report = evaluate_trajectory(trajectory, prompt_version=prompt_version)

    print(report.summary_line())
    print()
    for result in report.results:
        marker = "✓" if result.passed else "✗"
        severity_tag = result.severity.upper().ljust(5)
        print(f"  {marker} [{severity_tag}] {result.rule_id}: {result.message}")

    return 0 if report.passed else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate one trajectory.")
    parser.add_argument(
        "trajectory_path",
        help="Path to the trajectory JSON (e.g. data/trajectories/dark_knight_v2.json)",
    )
    args = parser.parse_args()
    sys.exit(main(args.trajectory_path))