# Throughline

Film recommendations by emotional trajectory, not metadata.

Most recommenders treat films as static points in feature space: "if you liked X,
you'll like Y." Throughline treats films as **vectors** — paths through emotional
space that take a viewer from one state to another. The match isn't "this film
is similar to that film." It's "this film will move you from where you are to
where you want to be."

The name is borrowed from screenwriting, where the *emotional throughline* is the
felt spine of a story — the line of motivation and feeling that runs from the
opening beat to the final frame. Each film here is analyzed into that throughline:
emotional beats placed at narrative positions (e.g. inciting incident at 8%,
first revelation at 22%, moral compromise at 64%, cathartic release at 91%).
Users target a destination via a hierarchical emotion vocabulary or by reference
("land me where Endgame's final battle lands"). Retrieval matches by trajectory
shape and endpoint, not by tags.

## Status

In progress — v1 in active development.

- [x] Project scoped, taxonomy v1 drafted, eval set of 15 films locked
- [x] Plot ingestion + LLM-driven emotional flagging pipeline
- [x] Versioned prompts with eval-driven iteration (v1 → v2 closed one loop on Dark Knight)
- [ ] Trajectory storage and vector retrieval
- [ ] Slider UI + trajectory line-graph visualization
- [ ] Natural-language query path (agent loop)
- [ ] MCP server exposing retrieval as a tool
- [ ] Eval harness
- [ ] Expand corpus to 50–100 films and ship public demo

## Stack

**Backend:** Python, FastAPI (async), PostgreSQL + pgvector, pytest
**LLM:** Anthropic Claude for emotional beat extraction and synthesis
**Frontend:** React + TypeScript + Vite, Tailwind, D3 for trajectory visualization
**Tooling:** MCP server for agentic retrieval

## Why this exists

Recommendation systems mostly optimize for similarity in feature space. That works
for "more of the same" but fails the question I actually want answered after a
film I loved: *what's the closest excitement?* — same emotional landing, different
film. Throughline is an attempt at that question.

## Notes

A writeup explaining the approach, evaluation methodology, and what worked vs.
what didn't will live in `/docs` once v1 ships. In the meantime,
`docs/findings/` contains per-film comparison notes documenting how the
flagging pipeline performs against the eval set — the first one is
`dark_knight_v1.md`.