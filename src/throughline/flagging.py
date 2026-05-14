"""LLM-driven film emotional trajectory flagging.

Given a film's plot synopsis, this pipeline produces a structured Trajectory
conforming to the v1 schema. The prompt and taxonomy are loaded from disk;
Claude does the extraction; Pydantic validates the response.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from anthropic import AsyncAnthropic
from pydantic import ValidationError

from throughline.schemas import Trajectory
from throughline.taxonomy import all_valid_tag_ids, taxonomy_as_prompt_text

# Repo root, used for locating prompt and plot files.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_PROMPTS_DIR = _REPO_ROOT / "prompts"
LATEST_PROMPT_VERSION = "v2"


def _prompt_path_for_version(version: str) -> Path:
    """Resolve a prompt version (e.g. 'v2') to the file on disk."""
    path = _PROMPTS_DIR / f"flag_film_{version}.md"
    if not path.exists():
        raise FlaggingError(
            f"Prompt version {version!r} not found at {path}. "
            f"Expected file: {path.name}"
        )
    return path

_MODEL = "claude-sonnet-4-5"
_MAX_TOKENS = 4000


class FlaggingError(Exception):
    """Raised when the LLM output cannot be parsed or validated."""

def _strip_markdown_fences(text: str) -> str:
    """Remove ```json ... ``` or ``` ... ``` wrappers if present.

    Claude sometimes wraps JSON output in markdown code fences despite
    explicit instructions otherwise. This is the cheapest safety net.
    Returns the text unchanged if no fences are present.
    """
    stripped = text.strip()
    if stripped.startswith("```"):
        first_newline = stripped.find("\n")
        if first_newline != -1:
            stripped = stripped[first_newline + 1 :]
    if stripped.endswith("```"):
        stripped = stripped[:-3].rstrip()
    return stripped.strip()

async def flag_film(
    film_id: str,
    film_title: str,
    year: int,
    plot_text: str,
    prompt_version: str = LATEST_PROMPT_VERSION,
) -> Trajectory:
    """Run the flagging pipeline on a single film.

    Parameters
    ----------
    film_id
        Snake-case identifier (e.g. "dark_knight"). Used as the trajectory's
        id and the output filename.
    film_title
        Display title (e.g. "The Dark Knight").
    year
        Release year.
    plot_text
        The plot synopsis to flag. Should be in narrative order, ideally
        2k–5k words.

    Returns
    -------
    A validated Trajectory object.

    Raises
    ------
    FlaggingError
        If the LLM output cannot be parsed as JSON, doesn't match the
        Trajectory schema, or contains tag IDs not in the taxonomy.
    """
    prompt_path = _prompt_path_for_version(prompt_version)
    prompt_template = prompt_path.read_text(encoding="utf-8")
    taxonomy_block = taxonomy_as_prompt_text()

    system_prompt = (
        f"{prompt_template}\n\n"
        f"## Taxonomy\n\n{taxonomy_block}"
    )

    user_message = (
        f"Film: {film_title} ({year})\n"
        f"Suggested film_id: {film_id}\n\n"
        f"## Plot synopsis\n\n{plot_text}"
    )

    client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = await client.messages.create(
        model=_MODEL,
        max_tokens=_MAX_TOKENS,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": "{"},
        ],
    )

    # Prefill makes the response start mid-JSON; re-add the opening brace.
    raw_output = "{" + response.content[0].text
    raw_output = _strip_markdown_fences(raw_output)

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        raise FlaggingError(
            f"Claude output was not valid JSON. First 200 chars: "
            f"{raw_output[:200]!r}"
        ) from exc

    try:
        trajectory = Trajectory.model_validate(parsed)
        # Stamp the trajectory with the prompt version that produced it.
        trajectory = trajectory.model_copy(update={"prompt_version": prompt_version})
    except ValidationError as exc:
        raise FlaggingError(
            f"Claude output failed schema validation:\n{exc}"
        ) from exc

    valid_ids = all_valid_tag_ids()
    used_ids = {tag for beat in trajectory.beats for tag in beat.tags}
    used_ids.update(trajectory.endpoint_tags)
    invalid_ids = used_ids - valid_ids
    if invalid_ids:
        raise FlaggingError(
            f"Claude returned tag IDs not in the taxonomy: {sorted(invalid_ids)}"
        )

    return trajectory