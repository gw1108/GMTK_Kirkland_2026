# GMTK Kirkland 2026

A 2D game built with **Godot 4.7** for the GMTK 2026 game jam (Kirkland team).

## Layout

- `game/` — the Godot project. Open this folder in the Godot editor, not the repo root.
- `design/` — game design documents. Source of truth for what to build.
- `SourceArt/` — source art and audio assets (indexed by the art-catalog skill).
- `tools/` — dev tooling, including `deploy-itch.ps1` (web export + itch.io upload via butler; set the game slug in `tools/itch-deploy.config.json`).
- `agent_play/` — game-agnostic AI playtest harness for Godot web builds (see its README; run `node agent_play/setup.mjs` once the game exists).
- `tasks/lessons.md` — running log of gotchas and lessons learned.

See `CLAUDE.md` for agent working conventions.
