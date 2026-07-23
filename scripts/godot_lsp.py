"""Minimal JSON-RPC client + server management for Godot's GDScript language server.

The Godot editor (GUI or --headless) serves LSP over TCP on 127.0.0.1:6005 by
default. This module speaks standard LSP framing (Content-Length headers) using
only the Python stdlib.

CLI:
    python scripts/godot_lsp.py status | start | stop [--host H] [--port P]

Env overrides: GODOT_EXE, GODOT_LSP_HOST, GODOT_LSP_PORT
"""
from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = REPO_ROOT / "game"
DEFAULT_HOST = os.environ.get("GODOT_LSP_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("GODOT_LSP_PORT", "6005"))
DEFAULT_GODOT = r"C:\Program Files\Godot\Godot_v4.7.1-stable_win64_console.exe"


def godot_exe() -> str:
    return os.environ.get("GODOT_EXE", DEFAULT_GODOT)


def path_to_uri(path) -> str:
    return Path(path).resolve().as_uri()


def norm_uri(uri: str) -> str:
    """Normalize a file:// URI or plain path so client paths and Godot's reply
    URIs (which percent-encode and lowercase the drive letter) compare equal."""
    if "://" in uri:
        path = unquote(urlparse(uri).path)
        if re.match(r"^/[A-Za-z]:", path):
            path = path[1:]
    else:
        path = uri
    return Path(path).resolve().as_posix().lower()


class LspClient:
    """A TCP LSP client. Not thread-safe; one request in flight at a time."""

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, timeout: float = 10.0):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self._buf = b""
        self._next_id = 0
        # Notifications received while waiting for a request's response.
        self.stashed: list[dict] = []

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass

    # -- framing ---------------------------------------------------------
    def _send(self, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.sock.sendall(b"Content-Length: " + str(len(body)).encode("ascii") + b"\r\n\r\n" + body)

    def read_message(self, timeout: float = 5.0):
        """Read one LSP message; returns a dict, or None on timeout (partial
        reads are buffered and resumed). Server->client *requests* are
        auto-answered with a null result so the server never stalls on us."""
        self.sock.settimeout(timeout)
        try:
            while True:
                header_end = self._buf.find(b"\r\n\r\n")
                if header_end != -1:
                    header = self._buf[:header_end].decode("ascii", "replace")
                    m = re.search(r"Content-Length:\s*(\d+)", header, re.I)
                    if not m:
                        raise ValueError(f"LSP frame without Content-Length: {header!r}")
                    length = int(m.group(1))
                    body_start = header_end + 4
                    if len(self._buf) >= body_start + length:
                        body = self._buf[body_start:body_start + length]
                        self._buf = self._buf[body_start + length:]
                        msg = json.loads(body.decode("utf-8"))
                        if "method" in msg and "id" in msg:  # server->client request
                            self._send({"jsonrpc": "2.0", "id": msg["id"], "result": None})
                        return msg
                chunk = self.sock.recv(65536)
                if not chunk:
                    raise ConnectionError("LSP server closed the connection")
                self._buf += chunk
        except socket.timeout:
            return None

    # -- rpc -------------------------------------------------------------
    def notify(self, method: str, params=None) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params or {}})

    def request(self, method: str, params=None, timeout: float = 30.0):
        self._next_id += 1
        rid = self._next_id
        self._send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}})
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            msg = self.read_message(timeout=min(2.0, max(0.1, deadline - time.monotonic())))
            if msg is None:
                continue
            if msg.get("id") == rid and ("result" in msg or "error" in msg):
                if "error" in msg:
                    raise RuntimeError(f"{method} failed: {msg['error']}")
                return msg["result"]
            if "method" in msg and "id" not in msg:
                self.stashed.append(msg)
        raise TimeoutError(f"no response to {method} within {timeout}s")

    # -- convenience -----------------------------------------------------
    def initialize(self, project_dir: Path = PROJECT_DIR):
        result = self.request("initialize", {
            "processId": os.getpid(),
            "clientInfo": {"name": "gmtk-godot-lsp-client"},
            "rootUri": path_to_uri(project_dir),
            "rootPath": str(project_dir),
            "capabilities": {},
        })
        self.notify("initialized", {})
        return result

    def did_open(self, path) -> str:
        """Open a .gd file on the server (required before most textDocument/*
        requests; triggers a publishDiagnostics notification). Returns the URI."""
        path = Path(path)
        uri = path_to_uri(path)
        self.notify("textDocument/didOpen", {"textDocument": {
            "uri": uri,
            "languageId": "gdscript",
            "version": 1,
            "text": path.read_text(encoding="utf-8"),
        }})
        return uri


def rpc(method: str, params=None, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
        boot: bool = True, open_files=()):
    """One-shot JSON-RPC call: ensures the server is up, handshakes, optionally
    opens files, sends `method` and returns its result."""
    ensure_server(host, port, boot=boot, quiet=True)
    client = LspClient(host, port)
    try:
        client.initialize()
        for f in open_files:
            client.did_open(f)
        return client.request(method, params)
    finally:
        client.close()


# -- server management ---------------------------------------------------
def port_open(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def ensure_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
                  boot: bool = True, wait: float = 120.0, quiet: bool = False) -> bool:
    """Return True once a server is listening. If nothing is on the port and
    `boot` is set, launch a detached headless Godot editor (it keeps running
    after this process exits; stop it with `python scripts/godot_lsp.py stop`)."""
    if port_open(host, port):
        return True
    if not boot:
        return False
    exe = godot_exe()
    if not Path(exe).exists():
        raise FileNotFoundError(f"Godot executable not found: {exe} (set GODOT_EXE)")
    if not quiet:
        print(f"[godot-lsp] booting headless Godot editor for {PROJECT_DIR} ...", flush=True)
    proc = subprocess.Popen(
        [exe, "--headless", "--editor", "--path", str(PROJECT_DIR)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    deadline = time.monotonic() + wait
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"Godot exited with code {proc.returncode} before serving LSP")
        if port_open(host, port):
            if not quiet:
                print("[godot-lsp] server is up", flush=True)
            return True
        time.sleep(0.5)
    proc.kill()
    raise TimeoutError(f"Godot LSP did not open port {port} within {wait}s")


def server_pid(port: int = DEFAULT_PORT):
    """PID of the process LISTENING on `port`, via netstat (Windows)."""
    out = subprocess.run(["netstat", "-ano", "-p", "TCP"], capture_output=True, text=True).stdout
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 5 and parts[3] == "LISTENING" and parts[1].endswith(f":{port}"):
            return int(parts[4])
    return None


def stop_server(port: int = DEFAULT_PORT) -> bool:
    """Kill the Godot process serving the LSP port. Refuses non-Godot PIDs."""
    pid = server_pid(port)
    if pid is None:
        return False
    q = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True).stdout
    if "godot" not in q.lower():
        raise RuntimeError(f"process {pid} on port {port} does not look like Godot; not killing it")
    subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True)
    return True


def _main(argv) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["status", "start", "stop"])
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = ap.parse_args(argv)

    if args.action == "status":
        pid = server_pid(args.port)
        up = port_open(args.host, args.port)
        print(f"LSP {'UP' if up else 'DOWN'} on {args.host}:{args.port}"
              + (f" (pid {pid})" if pid else ""))
        return 0 if up else 1
    if args.action == "start":
        ensure_server(args.host, args.port)
        print(f"LSP UP on {args.host}:{args.port} (pid {server_pid(args.port)})")
        return 0
    if args.action == "stop":
        if stop_server(args.port):
            print("stopped")
        else:
            print("nothing listening on that port")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
