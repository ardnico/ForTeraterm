"""TTL template rendering, validation, and linting."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from .storage import CommandSet, Profile


ALLOWED_AUTH_TYPES = {"password", "keyboard-interactive", "publickey"}


@dataclass
class TTLContext:
    """Render context passed into the TTL template."""

    host: str
    port: int
    user: str
    auth_type: str
    commands: List[str]
    ssh_options: str
    password: Optional[str]


class TTLRenderer:
    """Renders Tera Term macro files from templates and validates output."""

    def __init__(self, template_root: Path) -> None:
        self.template_root = template_root

    def validate_context(self, ctx: TTLContext) -> None:
        if not ctx.host or not ctx.user:
            raise ValueError("Host and user are required")
        if ctx.port <= 0:
            raise ValueError("Port must be positive")
        if ctx.auth_type not in ALLOWED_AUTH_TYPES:
            raise ValueError("Unsupported auth_type")
        for cmd in ctx.commands:
            if "\n" in cmd or "\r" in cmd:
                raise ValueError("Commands must be single-line")
            if cmd.strip() == "":
                raise ValueError("Commands cannot be empty")
            if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", cmd):
                raise ValueError("Commands contain control characters")
        if ctx.password and ("\n" in ctx.password or "\r" in ctx.password):
            raise ValueError("Password cannot contain newlines")
        if ctx.ssh_options and ("\n" in ctx.ssh_options or "\r" in ctx.ssh_options):
            raise ValueError("SSH options cannot contain newlines")

    def validate_output(self, ttl_content: str) -> None:
        lowered = ttl_content.lower()
        if "connect" not in lowered:
            raise ValueError("TTL script must call connect")
        if not lowered.strip().endswith("end"):
            raise ValueError("TTL script must end with 'end'")
        if re.search(r'sendln\s+"\s*"', ttl_content, re.IGNORECASE):
            raise ValueError("sendln statements must not be empty")

    def _escape(self, value: str) -> str:
        return value.replace('"', '""')

    def render(self, profile: Profile, command_set: CommandSet, password: Optional[str]) -> str:
        ctx = TTLContext(
            host=profile.host,
            port=profile.port,
            user=profile.user,
            auth_type=profile.auth_type,
            commands=command_set.commands,
            ssh_options=profile.ssh_options,
            password=password,
        )
        self.validate_context(ctx)
        template_path = self.template_root / "ttl" / "v1" / "basic.ttl.j2"
        template_text = template_path.read_text(encoding="utf-8")
        commands_block = [self._escape(cmd) for cmd in ctx.commands]
        passwd_flag = ""
        if ctx.password:
            passwd_flag = f" /passwd=\\\"{self._escape(ctx.password)}\\\""
        ssh_options = f" {self._escape(ctx.ssh_options.strip())}" if ctx.ssh_options.strip() else ""
        ttl_content = template_text.format(
            user=ctx.user,
            host=ctx.host,
            port=ctx.port,
            auth_type=ctx.auth_type,
            passwd_flag=passwd_flag,
            ssh_options=ssh_options,
            commands_block="\n".join(f'sendln "{cmd}"' for cmd in commands_block),
        )
        self.validate_output(ttl_content)
        return ttl_content


__all__ = ["TTLContext", "TTLRenderer", "ALLOWED_AUTH_TYPES"]
