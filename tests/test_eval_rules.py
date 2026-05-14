"""Tests for evaluation rules."""

from __future__ import annotations

import pytest

from throughline.eval.rules import (
    rule_beat_count_in_range,
    rule_beats_position_ordered,
    rule_dominant_register_represented,
    rule_ending_beat_exists,
    rule_endpoint_tags_appear_in_beats,
    rule_has_intensity_floor,
    rule_has_intensity_peak,
)
from throughline.eval.runner import evaluate_trajectory
from throughline.schemas import Beat, Trajectory


def _beat(
    position: float,
    *,
    tags: list[str] | None = None,
    intensity: float = 0.6,
) -> Beat:
    """Build a valid Beat with sensible defaults; only specify what matters."""
    return Beat(
        position=position,
        scene="test scene",
        tags=tags or ["dread.foreboding"],
        intensity=intensity,
        justification="test justification",
    )


def _trajectory(
    beats: list[Beat],
    *,
    endpoint_tags: list[str] | None = None,
    dominant_register: str = "dread",
) -> Trajectory:
    """Build a valid Trajectory from a list of beats."""
    return Trajectory(
        film_id="test_film",
        film_title="Test Film",
        year=2024,
        beats=beats,
        endpoint_tags=endpoint_tags or ["dread.foreboding"],
        dominant_register=dominant_register,
    )


# ---- rule_beat_count_in_range ----

def test_beat_count_passes_with_nine_beats() -> None:
    beats = [_beat(0.1 * i) for i in range(1, 10)]  # 9 beats at 0.1..0.9
    result = rule_beat_count_in_range(_trajectory(beats))
    assert result.passed
    assert result.severity == "error"


def test_beat_count_passes_at_boundary_six() -> None:
    beats = [_beat(0.1 * i) for i in range(1, 7)]
    assert rule_beat_count_in_range(_trajectory(beats)).passed


def test_beat_count_passes_at_boundary_twelve() -> None:
    beats = [_beat(0.05 * i) for i in range(1, 13)]
    assert rule_beat_count_in_range(_trajectory(beats)).passed


# Note: we cannot test count below 6 directly because the Trajectory
# schema rejects it on construction. Test that fact instead.
def test_trajectory_schema_rejects_fewer_than_four_beats() -> None:
    """Defense in depth: the schema's min_length should fire before the rule."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        _trajectory([_beat(0.5)])


# ---- rule_beats_position_ordered ----

def test_position_order_passes_when_ascending() -> None:
    beats = [_beat(0.1), _beat(0.3), _beat(0.5), _beat(0.9)]
    assert rule_beats_position_ordered(_trajectory(beats)).passed


# Position-order failures are also caught by the schema, so we test
# the schema rejection rather than feeding bad data to the rule.
def test_trajectory_schema_rejects_out_of_order_positions() -> None:
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        _trajectory(
            [_beat(0.1), _beat(0.5), _beat(0.3), _beat(0.9)]
        )


# ---- rule_endpoint_tags_appear_in_beats ----

def test_endpoint_tags_pass_when_all_appear_in_beats() -> None:
    beats = [
        _beat(0.1, tags=["dread.foreboding"]),
        _beat(0.5, tags=["grief.bereavement"]),
        _beat(0.7, tags=["triumph.victory"]),
        _beat(0.9, tags=["moral_weight.sacrifice"]),
    ]
    trajectory = _trajectory(
        beats,
        endpoint_tags=["moral_weight.sacrifice", "triumph.victory"],
    )
    assert rule_endpoint_tags_appear_in_beats(trajectory).passed


def test_endpoint_tags_fail_when_missing_from_beats() -> None:
    beats = [
        _beat(0.1, tags=["dread.foreboding"]),
        _beat(0.5, tags=["grief.bereavement"]),
        _beat(0.7, tags=["triumph.victory"]),
        _beat(0.9, tags=["moral_weight.sacrifice"]),
    ]
    trajectory = _trajectory(
        beats,
        endpoint_tags=["warmth.tenderness"],  # never appears in any beat
    )
    result = rule_endpoint_tags_appear_in_beats(trajectory)
    assert not result.passed
    assert "warmth.tenderness" in result.details["missing"]


# ---- rule_ending_beat_exists ----

def test_ending_beat_passes_when_last_beat_is_late() -> None:
    beats = [_beat(0.1), _beat(0.4), _beat(0.7), _beat(0.92)]
    assert rule_ending_beat_exists(_trajectory(beats)).passed


def test_ending_beat_fails_when_last_beat_is_too_early() -> None:
    beats = [_beat(0.1), _beat(0.4), _beat(0.6), _beat(0.75)]
    result = rule_ending_beat_exists(_trajectory(beats))
    assert not result.passed
    assert result.severity == "warn"


# ---- rule_has_intensity_peak ----

def test_intensity_peak_passes_when_a_beat_hits_threshold() -> None:
    beats = [
        _beat(0.1, intensity=0.4),
        _beat(0.5, intensity=0.6),
        _beat(0.7, intensity=0.95),
        _beat(0.9, intensity=0.7),
    ]
    assert rule_has_intensity_peak(_trajectory(beats)).passed


def test_intensity_peak_fails_when_all_beats_below_threshold() -> None:
    beats = [_beat(0.1 * i, intensity=0.6) for i in range(1, 8)]
    result = rule_has_intensity_peak(_trajectory(beats))
    assert not result.passed


# ---- rule_has_intensity_floor ----

def test_intensity_floor_passes_when_a_beat_is_quiet() -> None:
    beats = [
        _beat(0.1, intensity=0.3),
        _beat(0.5, intensity=0.7),
        _beat(0.7, intensity=0.9),
        _beat(0.9, intensity=0.8),
    ]
    assert rule_has_intensity_floor(_trajectory(beats)).passed


def test_intensity_floor_fails_when_all_beats_too_intense() -> None:
    beats = [_beat(0.1 * i, intensity=0.7) for i in range(1, 8)]
    result = rule_has_intensity_floor(_trajectory(beats))
    assert not result.passed


# ---- rule_dominant_register_represented ----

def test_dominant_register_passes_when_well_represented() -> None:
    # 4 beats, all tagged with dread.*; dominant_register="dread"
    beats = [
        _beat(0.1, tags=["dread.foreboding"]),
        _beat(0.4, tags=["dread.stakes"]),
        _beat(0.7, tags=["dread.visceral"]),
        _beat(0.9, tags=["dread.existential"]),
    ]
    trajectory = _trajectory(beats, dominant_register="dread")
    assert rule_dominant_register_represented(trajectory).passed


def test_dominant_register_fails_when_underrepresented() -> None:
    # 5 beats, only 1 has dread.*; dominant_register="dread"
    beats = [
        _beat(0.1, tags=["warmth.camaraderie"]),
        _beat(0.3, tags=["joy.hope"]),
        _beat(0.5, tags=["triumph.victory"]),
        _beat(0.7, tags=["dread.foreboding"]),
        _beat(0.9, tags=["warmth.tenderness"]),
    ]
    trajectory = _trajectory(beats, dominant_register="dread")
    result = rule_dominant_register_represented(trajectory)
    assert not result.passed
    assert result.details["fraction"] < 0.30


# ---- evaluate_trajectory orchestrator ----

def test_evaluate_trajectory_runs_all_rules() -> None:
    beats = [_beat(0.1 * i, intensity=0.6) for i in range(1, 8)]
    report = evaluate_trajectory(_trajectory(beats))
    rule_ids = [r.rule_id for r in report.results]
    assert "beat_count_in_range" in rule_ids
    assert "dominant_register_represented" in rule_ids
    assert len(report.results) == 7


def test_evaluate_trajectory_passes_when_only_warns_fail() -> None:
    # All errors pass, but intensity is uniform so peak/floor warns fail
    beats = [_beat(0.1 * i, intensity=0.6) for i in range(1, 8)]
    beats[-1] = _beat(0.92, intensity=0.6)  # ensure ending_beat_exists passes
    report = evaluate_trajectory(_trajectory(beats))
    assert report.passed  # errors all passed
    assert report.warn_count >= 1


def test_evaluate_trajectory_fails_on_error_severity_failure() -> None:
    # Endpoint tag missing from beats — error severity
    beats = [
        _beat(0.1, tags=["dread.foreboding"]),
        _beat(0.5, tags=["grief.bereavement"]),
        _beat(0.7, tags=["triumph.victory"]),
        _beat(0.95, tags=["moral_weight.sacrifice"]),
    ]
    trajectory = _trajectory(
        beats,
        endpoint_tags=["warmth.tenderness"],
    )
    report = evaluate_trajectory(trajectory)
    assert not report.passed
    assert report.error_count >= 1