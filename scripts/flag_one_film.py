"""CLI: flag one film and write the trajectory JSON to disk.

Usage:
    uv run python scripts/flag_one_film.py <film_id>

Reads:
    data/plots/raw/<film_id>.md         — plot synopsis with header
    prompts/flag_film_v1.md             — flagging prompt
    taxonomy/v1.json                    — emotion taxonomy

Writes:
    data/trajectories/<film_id>_v1.json — validated trajectory
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

from throughline.flagging import FlaggingError, flag_film

_REPO_ROOT = Path(__file__).resolve().parents[1]


def _parse_plot_file(path: Path) -> tuple[str, int, str]:
    """Extract the title, year, and body text from a plot markdown file.

    Expects a header like `# The Dark Knight (2008)` on the first line,
    followed by metadata, then a `---` separator, then the synopsis body.
    """
    text = path.read_text(encoding="utf-8")
    title_match = re.match(r"^#\s+(.+?)\s+\((\d{4})\)\s*$", text.split("\n")[0])
    if not title_match:
        raise ValueError(
            f"Could not parse title and year from first line of {path}. "
            f"Expected format: '# Title (YYYY)'."
        )
    title = title_match.group(1)
    year = int(title_match.group(2))

    if "---" in text:
        body = text.split("---", 1)[1].strip()
    else:
        body = text

    return title, year, body


async def main(film_id: str) -> int:
    load_dotenv()

    plot_path = _REPO_ROOT / "data" / "plots" / "raw" / f"{film_id}.md"
    if not plot_path.exists():
        print(f"ERROR: plot file not found: {plot_path}", file=sys.stderr)
        return 1

    print(f"Reading plot from {plot_path}")
    title, year, body = _parse_plot_file(plot_path)
    print(f"Parsed: {title} ({year}), {len(body.split())} words of synopsis")

    print(f"Calling Claude to flag {title}...")
    try:
        trajectory = await flag_film(
            film_id=film_id,
            film_title=title,
            year=year,
            plot_text=body,
        )
    except FlaggingError as exc:
        print(f"FLAGGING FAILED: {exc}", file=sys.stderr)
        return 2

    output_path = _REPO_ROOT / "data" / "trajectories" / f"{film_id}_v1.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(trajectory.model_dump(), f, indent=2, ensure_ascii=False)

    print(f"\nWrote trajectory to {output_path}")
    print(f"Beats: {len(trajectory.beats)}")
    print(f"Endpoint tags: {trajectory.endpoint_tags}")
    print(f"Dominant register: {trajectory.dominant_register}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flag one film.")
    parser.add_argument("film_id", help="snake_case film id, e.g. 'dark_knight'")
    args = parser.parse_args()
    sys.exit(asyncio.run(main(args.film_id)))