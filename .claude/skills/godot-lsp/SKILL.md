---
name: godot-lsp
description: Query the Godot GDScript language server via JSON-RPC (hover, symbols, definitions, diagnostics), manage the headless LSP server, and run the zero-warning audit on .gd files. Use for GDScript static analysis, symbol lookup, or checking warnings before committing.
---

# Godot LSP (GDScript language server)

The Godot editor serves LSP over TCP on `127.0.0.1:6005`. All tools below
auto-boot a headless editor (`--headless --editor --path game`) when nothing is
listening — first boot takes ~5–30s. If the developer has the Godot GUI editor
open with this project, it already serves 6005 and the tools just use it.

Env overrides: `GODOT_EXE`, `GODOT_LSP_HOST`, `GODOT_LSP_PORT`.

## Server management

```
python scripts/godot_lsp.py status|start|stop
```

The booted server stays alive between runs (that's intentional — keeps audits
fast). `stop` kills whatever Godot process is listening on the port.

## JSON-RPC function (agent API)

One invocation = one JSON-RPC call; handshake handled for you:

```
python scripts/lsp_rpc.py --uri-of game/player.gd            # build a file URI
python scripts/lsp_rpc.py --open game/player.gd textDocument/documentSymbol "{\"textDocument\":{\"uri\":\"<uri>\"}}"
python scripts/lsp_rpc.py --open game/player.gd textDocument/hover "{\"textDocument\":{\"uri\":\"<uri>\"},\"position\":{\"line\":4,\"character\":8}}"
```

- Most `textDocument/*` methods need the doc opened first: pass `--open FILE`
  (repeatable) and reference the same file's URI (from `--uri-of`) in params.
- Params: inline JSON or `@path/to/params.json`. `--notify` sends a
  notification instead of a request and prints server notifications
  (e.g. `textDocument/publishDiagnostics`) for ~2s.
- From Python: `from godot_lsp import rpc` (in `scripts/`):
  `rpc("textDocument/documentSymbol", {...}, open_files=["game/player.gd"])`.

## Zero-warning audit (LSP Audit)

All modified `.gd` files must have **zero** warnings/errors in the language
server. The pre-commit hook enforces this on staged files; run it manually:

```
python scripts/tests/audit_lsp_warnings.py --host 127.0.0.1 --port 6005 [files...]
python scripts/tests/audit_lsp_warnings.py --staged     # what the hook runs
python scripts/tests/audit_lsp_warnings.py              # all game/**/*.gd (addons excluded)
```

Exit 1 on any warning/error (severity ≤ 2). Fix warnings properly; use
`@warning_ignore(...)` only with explicit justification in a comment.

## Gotchas

- Diagnostics arrive as `publishDiagnostics` *notifications* after `didOpen`,
  not as a request response — the audit script handles the wait/collect.
- Godot's reply URIs percent-encode and lowercase the drive letter
  (`file:///c%3A/...`); `godot_lsp.norm_uri()` normalizes for comparison.
- A second Godot editor instance can't bind 6005 while one is running; the
  tools never boot when the port is already open, so this only matters if you
  start one by hand.
