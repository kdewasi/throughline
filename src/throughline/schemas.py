"""Pydantic schemas for film emotional trajectories.

These schemas define the contract between the LLM flagging pipeline and the
rest of the system. Every output produced by the flagging prompt must validate
against `Trajectory` or it is rejected.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class Beat(BaseModel):
    """A single tagged emotional moment in a film.

    Attributes
    ----------
    position : float
        Where in the film the beat occurs, expressed as a fraction of total
        narrative progression. 0.0 = opening frame, 1.0 = closing frame.
        v1 uses narrative percentage, not real timecodes.
    scene : str
        A short phrase identifying the scene (e.g. "Rachel's death",
        "ferry dilemma"). Used for human readability and eval comparison.
    tags : list[str]
        One or more tag IDs from the v1 taxonomy, in `superior.sub_emotion`
        form (e.g. "moral_weight.sacrifice"). Validated against the loaded
        taxonomy by the flagging pipeline, not by the schema itself.
    intensity : float
        Felt strength of the dominant emotion at this beat, on a 0.0–1.0
        scale. 0.3 = quiet, 0.6 = solid mid-film peak, 0.9 = climax-level.
    justification : str
        One short sentence explaining why this beat carries these tags. Used
        for prompt iteration and eval review — never shown to end users.
    """

    position: float = Field(ge=0.0, le=1.0)
    scene: str = Field(min_length=1, max_length=120)
    tags: list[str] = Field(min_length=1, max_length=4)
    intensity: float = Field(ge=0.0, le=1.0)
    justification: str = Field(min_length=1, max_length=300)

    @field_validator("tags")
    @classmethod
    def _tags_are_lowercase_dotted(cls, tags: list[str]) -> list[str]:
        """Reject tags that aren't in `superior.sub_emotion` lowercase form."""
        for tag in tags:
            if "." not in tag or tag != tag.lower():
                raise ValueError(
                    f"Tag {tag!r} must be in lowercase 'superior.sub_emotion' form"
                )
        return tags


class Trajectory(BaseModel):
    """The full emotional trajectory of a film.

    A film's trajectory is a sequence of beats ordered by narrative position,
    plus film-level metadata. The endpoint tags are the dominant tags of the
    final 5–10% of the film, used heavily by the matching algorithm.
    """

    film_id: str = Field(min_length=1, max_length=100)
    film_title: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=1900, le=2100)
    taxonomy_version: str = Field(default="1.0.0")
    prompt_version: str | None = Field(default=None, max_length=20)
    beats: list[Beat] = Field(min_length=4, max_length=20)
    endpoint_tags: list[str] = Field(min_length=1, max_length=4)
    dominant_register: str = Field(min_length=1, max_length=50)

    @field_validator("beats")
    @classmethod
    def _beats_are_position_ordered(cls, beats: list[Beat]) -> list[Beat]:
        """Reject trajectories whose beats aren't in ascending position order."""
        for earlier, later in zip(beats, beats[1:]):
            if later.position < earlier.position:
                raise ValueError(
                    "Beats must be ordered by ascending position; "
                    f"got {earlier.position} followed by {later.position}"
                )
        return beats