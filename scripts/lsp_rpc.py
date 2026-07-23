"""Send one JSON-RPC call to the Godot GDScript language server and print the reply.

This is the agent-facing API: one invocation = one JSON-RPC request (handshake
handled for you, server auto-booted if needed).

Examples (no JSON quoting needed for the common cases):
    python scripts/lsp_rpc.py --open game/player.gd textDocument/documentSymbol
    python scripts/lsp_rpc.py --open game/player.gd textDocument/hover --pos 5:9
    python scripts/lsp_rpc.py --open game/player.gd textDocument/definition --pos 12:20
    python scripts/lsp_rpc.py --uri-of game/player.gd
    python scripts/lsp_rpc.py textDocument/documentSymbol @params.json

Notes:
    - Most textDocument/* methods require the doc to be opened first: pass
      --open FILE (repeatable).
    - When params are omitted, {"textDocument": {"uri": <first --open file>}}
      is used automatically; --pos LINE:COL (1-based) merges in a position.
    - Explicit params may be inline JSON or @path/to/params.json — prefer the
      @file form on Windows, shells mangle inline JSON quoting.
    - --notify sends a notification instead of a request and then prints any
      server notifications (e.g. textDocument/publishDiagnostics) for ~2s.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from godot_lsp import (  # noqa: E402
    DEFAULT_HOST, DEFAULT_PORT, LspClient, ensure_server, path_to_uri,
)


def _parse_params(raw, open_files, pos):
    if raw is None or raw == "":
        params = {}
        if open_files:
            params["textDocument"] = {"uri": path_to_uri(open_files[0])}
    else:
        if raw.startswith("@"):
            raw = Path(raw[1:]).read_text(encoding="utf-8")
        params = json.loads(raw)
    if pos:
        line, _, col = pos.partition(":")
        params["position"] = {"line": int(line) - 1, "character": int(col or 1) - 1}
    return params


def main(argv) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("method", nargs="?", help="JSON-RPC method, e.g. textDocument/documentSymbol")
    ap.add_argument("params", nargs="?", help="params as inline JSON or @file.json (default {})")
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--open", action="append", default=[], metavar="FILE",
                    help="send textDocument/didOpen for FILE before the call (repeatable)")
    ap.add_argument("--pos", metavar="LINE:COL",
                    help="1-based position merged into params (for hover/definition/completion)")
    ap.add_argument("--notify", action="store_true", help="send a notification instead of a request")
    ap.add_argument("--no-boot", dest="boot", action="store_false",
                    help="fail instead of booting a headless editor when the server is down")
    ap.add_argument("--timeout", type=float, default=30.0)
    ap.add_argument("--uri-of", metavar="PATH", help="print the file:// URI for PATH and exit")
    args = ap.parse_args(argv)

    if args.uri_of:
        print(path_to_uri(args.uri_of))
        return 0
    if not args.method:
        ap.error("method is required (or use --uri-of)")

    params = _parse_params(args.params, args.open, args.pos)

    if not ensure_server(args.host, args.port, boot=args.boot, quiet=True):
        print(f"error: no LSP server on {args.host}:{args.port} (and --no-boot given)", file=sys.stderr)
        return 1

    client = LspClient(args.host, args.port)
    try:
        client.initialize()
        for f in args.open:
            client.did_open(f)
        if args.notify:
            client.notify(args.method, params)
            deadline = time.monotonic() + 2.0
            while time.monotonic() < deadline:
                msg = client.read_message(timeout=0.5)
                if msg and "method" in msg:
                    print(json.dumps(msg, indent=2))
        else:
            result = client.request(args.method, params, timeout=args.timeout)
            print(json.dumps(result, indent=2))
        return 0
    except (RuntimeError, TimeoutError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
