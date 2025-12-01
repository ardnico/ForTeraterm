"""Launcher responsible for rendering TTL, invoking Tera Term, and recording results."""

from __future__ import annotations

import datetime as dt
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .credential_store import Credential
from .storage import CommandSet, DataStore, HistoryRecord, Profile
from .ttl_renderer import TTLRenderer


@dataclass
class LaunchResult:
    result: str
    error_code: Optional[str]
    wlog_path: Path


class Launcher:
    """Coordinates TTL generation, execution (stubbed), and history recording."""

    def __init__(self, renderer: TTLRenderer, storage: DataStore, stub_mode: bool = True) -> None:
        self.renderer = renderer
        self.storage = storage
        self.stub_mode = stub_mode

    def launch(
        self,
        profile: Profile,
        command_set: CommandSet,
        credential: Optional[Credential],
        password_fallback: Optional[str],
    ) -> LaunchResult:
        password = credential.secret if credential else password_fallback
        ttl_file: Optional[Path] = None
        wlog_path: Optional[Path] = None
        try:
            ttl_content = self.renderer.render(profile, command_set, password)
            ttl_file = self._write_ttl(ttl_content)
            wlog_path = ttl_file.with_suffix(".wlog")
        except Exception:
            # TTL lint/rendering failure
            self._record_history(
                profile,
                command_set,
                result="failed",
                error_code="ttl_lint_failed",
                error_message="TTL validation failed",
                wlog_path=None,
            )
            raise
        try:
            if self.stub_mode:
                self._run_stub(profile, command_set, password, ttl_file, wlog_path)
            else:
                raise NotImplementedError("Real Tera Term execution not implemented in this environment")
            error_code = self._analyze_wlog(wlog_path)
            result = "success" if error_code is None else "failed"
        except Exception:
            self._record_history(
                profile,
                command_set,
                result="failed",
                error_code="launch_failed",
                error_message="Stub/launcher failure",
                wlog_path=wlog_path,
            )
            raise
        finally:
            if ttl_file:
                try:
                    ttl_file.unlink()
                except FileNotFoundError:
                    pass
        self._record_history(
            profile,
            command_set,
            result=result,
            error_code=error_code,
            error_message=error_code,
            wlog_path=wlog_path,
        )
        return LaunchResult(result=result, error_code=error_code, wlog_path=wlog_path or Path(""))

    def _write_ttl(self, content: str) -> Path:
        fd, path_str = tempfile.mkstemp(prefix="tt-launch-", suffix=".ttl")
        os.close(fd)
        ttl_file = Path(path_str)
        ttl_file.write_text(content, encoding="utf-8")
        return ttl_file

    def _run_stub(
        self, profile: Profile, command_set: CommandSet, password: Optional[str], ttl_file: Path, wlog: Path
    ) -> None:
        lines = [
            f"Connecting to {profile.host}:{profile.port} as {profile.user}",
            "Using stub mode - not invoking Tera Term",
            f"TTL file: {ttl_file}",
        ]
        if profile.auth_type == "password" and not password:
            lines.append("Login failed: missing password")
        elif password == "bad" or profile.host.startswith("invalid"):
            lines.append("Login failed")
        else:
            lines.append("Login successful")
            for cmd in command_set.commands:
                lines.append(f"RUN: {cmd}")
            lines.append("OK_FROM_SERVER")
        wlog.write_text("\n".join(lines), encoding="utf-8")

    def _analyze_wlog(self, wlog_path: Path) -> Optional[str]:
        content = wlog_path.read_text(encoding="utf-8")
        lowered = content.lower()
        if "login failed" in lowered or "permission denied" in lowered:
            return "login_failed"
        if "connection refused" in lowered or "name or service not known" in lowered:
            return "connect_failed"
        if "command not found" in lowered:
            return "command_failed"
        if "ok_from_server" in lowered:
            return None
        return "wlog_unknown"

    def _record_history(
        self,
        profile: Profile,
        command_set: CommandSet,
        result: str,
        error_code: Optional[str],
        error_message: Optional[str],
        wlog_path: Optional[Path],
    ) -> None:
        record = HistoryRecord(
            id=None,
            profile_id=profile.id or 0,
            command_set_id=command_set.id,
            connected_at=dt.datetime.utcnow().isoformat(),
            result=result,
            error_code=error_code,
            error_message_short=error_message,
            ttl_template_version=profile.ttl_template_version,
            wlog_path=str(wlog_path) if wlog_path else None,
        )
        self.storage.record_history(record)


__all__ = ["LaunchResult", "Launcher"]
