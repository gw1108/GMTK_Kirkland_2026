---
name: art-catalog
description: Build or refresh the searchable catalog of art assets under SourceArt/ — index images, generate labeled contact sheets, write vision descriptions, and wire the catalog into CLAUDE.md. Use when new art is added, when asked to catalog/index art assets, or when pending source-art updates need review.
---

# Art Catalog

This work runs in the dedicated `art-catalog` subagent (defined in `.claude/agents/art-catalog.md`, pinned to Sonnet) so cataloging runs don't pollute the main context.

**Do not perform the cataloging inline.** Launch the subagent via the Agent tool with `subagent_type: "art-catalog"`, passing along any user-provided specifics (custom `--root`, scope, whether to only resolve pending updates). The agent handles scan → describe → annotate → verify → report; relay its final report (counts and any unresolved `pending_updates` entries) back to the user.
