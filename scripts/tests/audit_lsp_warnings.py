"""Audit .gd files for GDScript errors/warnings via the Godot language server.

Zero-warning compliance gate: exits non-zero if any audited file has an error
or warning diagnostic (LSP severity 1 or 2), or if the server never reported
diagnostics for a file within the timeout.

Usage:
    python scripts/tests/audit_lsp_warnings.py --host 127.0.0.1 --port 6005 [files...]
    python scripts/tests/audit_lsp_warnings.py --staged     # staged .gd files (pre-commit)

With no files and no --staged, audits every .gd under game/ (addons/ and
.godot/ excluded). Boots a headless Godot editor automatically if no LSP server
is listening; the booted server is left running for fast subsequent runs
(stop it with `python scripts/godot_lsp.py stop`).
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from godot_lsp import (  # noqa: E402
    DEFAULT_HOST, DEFAULT_PORT, PROJECT_DIR, REPO_ROOT,
    LspClient, ensure_server, norm_uri, port_open, stop_server,
)

SEVERITY_NAMES = {1: "ERROR", 2: "WARNING", 3: "INFO", 4: "HINT"}


def staged_gd_files() -> list[Path]:
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "--", "*.gd"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    ).stdout
    return [REPO_ROOT / line.strip() for line in out.splitlines() if line.strip()]


def all_project_gd_files() -> list[Path]:
    return sorted(
        p for p in PROJECT_DIR.rglob("*.gd")
        if "addons" not in p.parts and ".godot" not in p.parts
    )


def main(argv) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="specific .gd files to audit")
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--staged", action="store_true", help="audit staged .gd files (for pre-commit)")
    ap.add_argument("--boot", action="store_true", default=True,
                    help="boot a headless editor if no server is up (default)")
    ap.add_argument("--no-boot", dest="boot", action="store_false")
    ap.add_argument("--shutdown", action="store_true",
                    help="stop the server after the audit if this run booted it")
    ap.add_argument("--timeout", type=float, default=None,
                    help="seconds to wait for diagnostics (default: 15 + 2/file)")
    args = ap.parse_args(argv)

    if args.staged:
        files = staged_gd_files()
    elif args.files:
        files = [Path(f).resolve() for f in args.files]
    else:
        files = all_project_gd_files()

    if not files:
        print("[lsp-audit] no .gd files to audit -- OK")
        return 0
    missing = [f for f in files if not f.is_file()]
    if missing:
        for f in missing:
            print(f"[lsp-audit] no such file: {f}", file=sys.stderr)
        return 2

    was_running = port_open(args.host, args.port)
    if not ensure_server(args.host, args.port, boot=args.boot):
        print(f"[lsp-audit] no LSP server on {args.host}:{args.port} (and --no-boot given)", file=sys.stderr)
        return 2

    print(f"[lsp-audit] auditing {len(files)} file(s) against {args.host}:{args.port}")
    timeout = args.timeout if args.timeout is not None else 15.0 + 2.0 * len(files)

    results: dict[str, list] = {}      # norm path -> diagnostics
    pending: dict[str, Path] = {norm_uri(str(f)): f for f in files}

    def handle(msg) -> None:
        if msg.get("method") != "textDocument/publishDiagnostics":
            return
        p = msg.get("params", {})
        key = norm_uri(p.get("uri", ""))
        if key in pending:
            results[key] = p.get("diagnostics", [])
            del pending[key]

    client = LspClient(args.host, args.port)
    try:
        client.initialize()
        for f in files:
            client.did_open(f)
        for msg in client.stashed:
            handle(msg)
        deadline = time.monotonic() + timeout
        while pending and time.monotonic() < deadline:
            msg = client.read_message(timeout=1.0)
            if msg:
                handle(msg)
    finally:
        client.close()
        if args.shutdown and not was_running:
            stop_server(args.port)

    failed = 0
    total_diags = 0
    for f in files:
        try:
            rel = f.relative_to(REPO_ROOT)
        except ValueError:
            rel = f
        key = norm_uri(str(f))
        if key not in results:
            print(f"{rel}: FAILED -- no diagnostics received within {timeout:.0f}s")
            failed += 1
            continue
        diags = results[key]
        for d in diags:
            sev = SEVERITY_NAMES.get(d.get("severity", 1), "?")
            start = d.get("range", {}).get("start", {})
            line, col = start.get("line", 0) + 1, start.get("character", 0) + 1
            code = d.get("code", "")
            code_s = f" [{code}]" if code else ""
            print(f"{rel}:{line}:{col}: {sev}{code_s}: {d.get('message', '').strip()}")
        total_diags += len(diags)
        if any(d.get("severity", 1) <= 2 for d in diags):
            failed += 1

    if failed:
        print(f"[lsp-audit] FAIL -- {failed}/{len(files)} file(s) with errors/warnings "
              f"(zero-warning compliance required)")
        return 1
    print(f"[lsp-audit] OK -- {len(files)} file(s) clean"
          + (f" ({total_diags} info/hint diagnostics)" if total_diags else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
