"""TTL template rendering, validation, and linting."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from .storage import CommandSet, Profile


@dataclass
class TTLContext:
    """Render context passed into the TTL template."""

    host: str
    port: int
    user: str
    auth_type: str
    commands: List[str]
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
        if ctx.auth_type not in {"password", "keyboard-interactive", "publickey"}:
            raise ValueError("Unsupported auth_type")
        for cmd in ctx.commands:
            if "\n" in cmd or "\r" in cmd:
                raise ValueError("Commands must be single-line")
            if cmd.strip() == "":
                raise ValueError("Commands cannot be empty")

    def validate_output(self, ttl_content: str) -> None:
        if "connect" not in ttl_content:
            raise ValueError("TTL script must call connect")
        if not ttl_content.strip().lower().endswith("end"):
            raise ValueError("TTL script must end with 'end'")

    def render(self, profile: Profile, command_set: CommandSet, password: Optional[str]) -> str:
        ctx = TTLContext(
            host=profile.host,
            port=profile.port,
            user=profile.user,
            auth_type=profile.auth_type,
            commands=command_set.commands,
            password=password,
        )
        self.validate_context(ctx)
        template_path = self.template_root / "ttl" / "v1" / "basic.ttl.j2"
        escaped_commands = []
        for cmd in ctx.commands:
            escaped = cmd.replace('"', '""')
            escaped_commands.append(f'sendln "{escaped}"')
        commands_block = "\n".join(escaped_commands)
        passwd_flag = ""
        if ctx.password:
            escaped = ctx.password.replace('"', '""')
            passwd_flag = f" /passwd=\\\"{escaped}\\\""
        template_text = template_path.read_text(encoding="utf-8")
        ttl_content = template_text.format(
            user=ctx.user,
            host=ctx.host,
            port=ctx.port,
            auth_type=ctx.auth_type,
            passwd_flag=passwd_flag,
            commands_block=commands_block,
        )
        self.validate_output(ttl_content)
        return ttl_content


__all__ = ["TTLContext", "TTLRenderer"]
