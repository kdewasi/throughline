"""Loader for the v1 emotion taxonomy."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

# The taxonomy file lives at the repo root, two levels above this file
# (src/throughline/taxonomy.py -> repo root).
_TAXONOMY_PATH = Path(__file__).resolve().parents[2] / "taxonomy" / "v1.json"


@lru_cache(maxsize=1)
def load_taxonomy() -> dict[str, Any]:
    """Load and cache the v1 emotion taxonomy from disk.

    Cached for the lifetime of the process. Raises if the file is missing
    or malformed.
    """
    with _TAXONOMY_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def all_valid_tag_ids() -> set[str]:
    """Return the set of all valid `superior.sub_emotion` tag IDs.

    Used by the flagging pipeline to validate Claude's output against the
    actual taxonomy contents (the schema only checks tag *shape*, not whether
    a tag exists in the taxonomy).
    """
    taxonomy = load_taxonomy()
    return {
        sub["id"]
        for superior in taxonomy["superior_emotions"]
        for sub in superior["sub_emotions"]
    }


def taxonomy_as_prompt_text() -> str:
    """Render the taxonomy as a human-readable block to embed in the prompt.

    Returns a markdown-formatted string listing every superior emotion, its
    sub-emotions, and their glosses. This is the form the LLM sees.
    """
    taxonomy = load_taxonomy()
    lines: list[str] = []
    for superior in taxonomy["superior_emotions"]:
        lines.append(f"### {superior['name']} ({superior['id']})")
        lines.append(f"_{superior['gloss']}_")
        lines.append("")
        for sub in superior["sub_emotions"]:
            lines.append(f"- `{sub['id']}` — **{sub['name']}**: {sub['gloss']}")
        lines.append("")
    return "\n".join(lines).strip()