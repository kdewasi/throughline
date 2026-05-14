"""Evaluation rules checked against flagging pipeline output.

Each rule is a pure function: takes a Trajectory, returns a RuleResult.
Rules are registered in ALL_RULES (bottom of file) so the runner can
iterate them.
"""

from __future__ import annotations

from collections import Counter
from typing import Callable

from throughline.eval.schemas import RuleResult
from throughline.schemas import Trajectory

# Type alias for clarity: a rule is a function from Trajectory to RuleResult.
Rule = Callable[[Trajectory], RuleResult]

_MIN_BEATS = 6
_MAX_BEATS = 12
_ENDING_POSITION_THRESHOLD = 0.85
_PEAK_INTENSITY_THRESHOLD = 0.85
_FLOOR_INTENSITY_THRESHOLD = 0.4
_DOMINANT_REGISTER_FRACTION = 0.30


def rule_beat_count_in_range(trajectory: Trajectory) -> RuleResult:
    """Trajectory has between 6 and 12 beats inclusive."""
    count = len(trajectory.beats)
    passed = _MIN_BEATS <= count <= _MAX_BEATS
    return RuleResult(
        rule_id="beat_count_in_range",
        severity="error",
        passed=passed,
        message=(
            f"Beat count is {count}; expected {_MIN_BEATS}–{_MAX_BEATS}."
            if not passed
            else f"Beat count {count} is in range."
        ),
        details={"count": count, "min": _MIN_BEATS, "max": _MAX_BEATS},
    )


def rule_beats_position_ordered(trajectory: Trajectory) -> RuleResult:
    """Beats appear in ascending order of position.

    The schema already enforces this on construction, but we re-check at
    the eval layer for defense in depth — schemas could change, this
    rule shouldn't go silent.
    """
    positions = [beat.position for beat in trajectory.beats]
    out_of_order = [
        (i, positions[i], positions[i + 1])
        for i in range(len(positions) - 1)
        if positions[i + 1] < positions[i]
    ]
    passed = not out_of_order
    return RuleResult(
        rule_id="beats_position_ordered",
        severity="error",
        passed=passed,
        message=(
            "Beats are in ascending position order."
            if passed
            else f"Found {len(out_of_order)} out-of-order beat pair(s)."
        ),
        details={"out_of_order_pairs": out_of_order},
    )


def rule_endpoint_tags_appear_in_beats(trajectory: Trajectory) -> RuleResult:
    """Every endpoint tag must also appear in at least one beat's tags.

    Endpoint tags are supposed to summarize the final 5–10% of the film.
    If the model invents an endpoint tag that doesn't appear anywhere
    else in the trajectory, that's an inconsistency.
    """
    beat_tags = {tag for beat in trajectory.beats for tag in beat.tags}
    missing = [tag for tag in trajectory.endpoint_tags if tag not in beat_tags]
    passed = not missing
    return RuleResult(
        rule_id="endpoint_tags_appear_in_beats",
        severity="error",
        passed=passed,
        message=(
            "All endpoint tags appear in at least one beat."
            if passed
            else f"Endpoint tags missing from beats: {missing}"
        ),
        details={"missing": missing},
    )


def rule_ending_beat_exists(trajectory: Trajectory) -> RuleResult:
    """At least one beat is positioned in the final 15% of the film.

    Heuristic: an ending must be flagged. If the latest beat is below
    0.85 the model may have failed to identify the ending.
    """
    max_position = max(beat.position for beat in trajectory.beats)
    passed = max_position >= _ENDING_POSITION_THRESHOLD
    return RuleResult(
        rule_id="ending_beat_exists",
        severity="warn",
        passed=passed,
        message=(
            f"Latest beat at position {max_position:.2f} (>= "
            f"{_ENDING_POSITION_THRESHOLD})."
            if passed
            else f"No beat in the final 15%; latest is at {max_position:.2f}."
        ),
        details={"max_position": max_position, "threshold": _ENDING_POSITION_THRESHOLD},
    )


def rule_has_intensity_peak(trajectory: Trajectory) -> RuleResult:
    """At least one beat has intensity >= 0.85.

    Heuristic: every film should have a moment of peak emotion. A
    trajectory with all beats below 0.85 is suspect — the model may have
    flattened the emotional range.
    """
    max_intensity = max(beat.intensity for beat in trajectory.beats)
    passed = max_intensity >= _PEAK_INTENSITY_THRESHOLD
    return RuleResult(
        rule_id="has_intensity_peak",
        severity="warn",
        passed=passed,
        message=(
            f"Peak intensity is {max_intensity:.2f}."
            if passed
            else f"No beat at peak intensity; highest is {max_intensity:.2f}."
        ),
        details={"max_intensity": max_intensity, "threshold": _PEAK_INTENSITY_THRESHOLD},
    )


def rule_has_intensity_floor(trajectory: Trajectory) -> RuleResult:
    """At least one beat has intensity <= 0.4.

    Heuristic: most films have at least one quiet beat for contrast. A
    trajectory where every beat is mid-to-high intensity is suspect —
    the model may be treating every scene as climactic.
    """
    min_intensity = min(beat.intensity for beat in trajectory.beats)
    passed = min_intensity <= _FLOOR_INTENSITY_THRESHOLD
    return RuleResult(
        rule_id="has_intensity_floor",
        severity="warn",
        passed=passed,
        message=(
            f"Floor intensity is {min_intensity:.2f}."
            if passed
            else f"No quiet beat; lowest is {min_intensity:.2f}."
        ),
        details={"min_intensity": min_intensity, "threshold": _FLOOR_INTENSITY_THRESHOLD},
    )


def rule_dominant_register_represented(trajectory: Trajectory) -> RuleResult:
    """The dominant register superior emotion appears in >= 30% of beat tags.

    Heuristic: if Claude claims the film's dominant register is `dread`
    but only 1 of 10 beats uses any dread tag, the claim is unsupported.
    A consistent dominant register should be visible in the beat tagging.
    """
    dominant = trajectory.dominant_register
    all_superiors = [
        tag.split(".", 1)[0] for beat in trajectory.beats for tag in beat.tags
    ]
    if not all_superiors:
        return RuleResult(
            rule_id="dominant_register_represented",
            severity="warn",
            passed=False,
            message="Trajectory has no beat tags to evaluate.",
            details={},
        )
    counts = Counter(all_superiors)
    dominant_count = counts.get(dominant, 0)
    fraction = dominant_count / len(all_superiors)
    passed = fraction >= _DOMINANT_REGISTER_FRACTION
    return RuleResult(
        rule_id="dominant_register_represented",
        severity="warn",
        passed=passed,
        message=(
            f"Dominant register '{dominant}' represented in "
            f"{fraction:.0%} of beat tags."
            if passed
            else f"Dominant register '{dominant}' only in "
            f"{fraction:.0%} of beat tags (expected >= "
            f"{_DOMINANT_REGISTER_FRACTION:.0%})."
        ),
        details={
            "dominant": dominant,
            "fraction": fraction,
            "threshold": _DOMINANT_REGISTER_FRACTION,
            "superior_counts": dict(counts),
        },
    )


# Registry of all rules. The runner iterates this list.
ALL_RULES: list[Rule] = [
    rule_beat_count_in_range,
    rule_beats_position_ordered,
    rule_endpoint_tags_appear_in_beats,
    rule_ending_beat_exists,
    rule_has_intensity_peak,
    rule_has_intensity_floor,
    rule_dominant_register_represented,
]