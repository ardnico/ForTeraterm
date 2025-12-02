from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class PortForward:
    local_port: str
    remote_host: str
    remote_port: str


def parse_ssh_options(ssh_options: str) -> Tuple[List[PortForward], str]:
    forwards: List[PortForward] = []
    extras: list[str] = []
    for token in ssh_options.split():
        if token.upper().startswith("/FWD=") and "=" in token:
            payload = token[5:]
            if "=" in payload and ":" in payload:
                try:
                    local, rest = payload.split("=", 1)
                    remote_host, remote_port = rest.split(":", 1)
                except ValueError:
                    extras.append(token)
                    continue
                forwards.append(PortForward(local_port=local, remote_host=remote_host, remote_port=remote_port))
            else:
                extras.append(token)
        elif token:
            extras.append(token)
    return forwards, " ".join(extras).strip()


def build_ssh_options(forwards: List[PortForward], extra_options: str) -> str:
    tokens: list[str] = []
    for forward in forwards:
        if forward.local_port and forward.remote_host and forward.remote_port:
            tokens.append(f"/FWD={forward.local_port}={forward.remote_host}:{forward.remote_port}")
    if extra_options.strip():
        tokens.append(extra_options.strip())
    return " ".join(tokens).strip()


__all__ = ["PortForward", "parse_ssh_options", "build_ssh_options"]
