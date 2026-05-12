"""Tests for the trajectory schemas."""

import pytest
from pydantic import ValidationError

from throughline.schemas import Beat, Trajectory


def _valid_beat(**overrides) -> dict:
    """Return a minimal valid Beat as a dict, with overrides applied."""
    return {
        "position": 0.5,
        "scene": "test scene",
        "tags": ["dread.foreboding"],
        "intensity": 0.7,
        "justification": "a reason",
    } | overrides


def test_beat_accepts_valid_input() -> None:
    Beat(**_valid_beat())


def test_beat_rejects_position_above_one() -> None:
    with pytest.raises(ValidationError):
        Beat(**_valid_beat(position=1.5))


def test_beat_rejects_uppercase_tag() -> None:
    with pytest.raises(ValidationError):
        Beat(**_valid_beat(tags=["Dread.Foreboding"]))


def test_beat_rejects_tag_without_dot() -> None:
    with pytest.raises(ValidationError):
        Beat(**_valid_beat(tags=["foreboding"]))


def test_trajectory_rejects_out_of_order_beats() -> None:
    beats = [
        Beat(**_valid_beat(position=0.6)),
        Beat(**_valid_beat(position=0.3)),  # earlier than the one before
        Beat(**_valid_beat(position=0.5)),
        Beat(**_valid_beat(position=0.9)),
    ]
    with pytest.raises(ValidationError):
        Trajectory(
            film_id="test",
            film_title="Test",
            year=2024,
            beats=beats,
            endpoint_tags=["joy.delight"],
            dominant_register="joy",
        )


def test_trajectory_rejects_too_few_beats() -> None:
    beats = [Beat(**_valid_beat(position=0.5))]  # only 1, need at least 4
    with pytest.raises(ValidationError):
        Trajectory(
            film_id="test",
            film_title="Test",
            year=2024,
            beats=beats,
            endpoint_tags=["joy.delight"],
            dominant_register="joy",
        )


def test_trajectory_accepts_valid_input() -> None:
    beats = [
        Beat(**_valid_beat(position=0.05, scene="opening")),
        Beat(**_valid_beat(position=0.40, scene="midpoint")),
        Beat(**_valid_beat(position=0.75, scene="climax build")),
        Beat(**_valid_beat(position=0.95, scene="ending")),
    ]
    trajectory = Trajectory(
        film_id="test_2024",
        film_title="Test",
        year=2024,
        beats=beats,
        endpoint_tags=["joy.delight", "warmth.tenderness"],
        dominant_register="joy",
    )
    assert len(trajectory.beats) == 4
    assert trajectory.taxonomy_version == "1.0.0"