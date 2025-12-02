"""Launcher responsible for rendering TTL, invoking Tera Term, and recording results."""

from __future__ import annotations

import datetime as dt
import os
import socket
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from .credential_store import Credential
from .storage import CommandSet, DataStore, HistoryRecord, Profile
from .ttl_renderer import TTLRenderer


@dataclass
class LaunchResult:
    result: str
    error_code: Optional[str]
    wlog_path: Path
    attempts: int = 1


@dataclass
class LaunchSession:
    """Represents an asynchronous launch session."""

    thread: threading.Thread
    cancel_event: threading.Event
    timeout_s: float

    def cancel(self) -> None:
        self.cancel_event.set()
        if self.thread.is_alive():
            self.thread.join(timeout=0.1)


class Launcher:
    """Coordinates TTL generation, execution (stubbed), and history recording."""

    def __init__(
        self,
        renderer: TTLRenderer,
        storage: DataStore,
        stub_mode: bool = True,
        preflight_check: Optional[Callable[[Profile], tuple[bool, str]]] = None,
    ) -> None:
        self.renderer = renderer
        self.storage = storage
        self.stub_mode = stub_mode
        self.preflight_check = preflight_check or self._default_preflight

    def launch(
        self,
        profile: Profile,
        command_set: CommandSet,
        credential: Optional[Credential],
        password_fallback: Optional[str],
        *,
        timeout_s: float = 30.0,
        max_retries: int = 0,
    ) -> LaunchResult:
        """Synchronous launch wrapper around the async pipeline."""
        result_holder: list[LaunchResult] = []
        done = threading.Event()

        def capture(result: LaunchResult) -> None:
            result_holder.append(result)
            done.set()

        session = self.launch_async(
            profile,
            command_set,
            credential,
            password_fallback,
            on_output=None,
            on_complete=capture,
            timeout_s=timeout_s,
            max_retries=max_retries,
        )
        done.wait(timeout=timeout_s + 5)
        session.cancel()
        if not result_holder:
            raise TimeoutError("Launch did not complete")
        return result_holder[0]

    def launch_async(
        self,
        profile: Profile,
        command_set: CommandSet,
        credential: Optional[Credential],
        password_fallback: Optional[str],
        *,
        on_output: Optional[Callable[[str], None]],
        on_complete: Callable[[LaunchResult], None],
        timeout_s: float = 30.0,
        max_retries: int = 0,
    ) -> LaunchSession:
        """Launch without blocking the caller, streaming output via callback."""
        password = credential.secret if credential else password_fallback
        cancel_event = threading.Event()

        def runner() -> None:
            attempts = 0
            last_result: LaunchResult | None = None
            while attempts <= max_retries and not cancel_event.is_set():
                attempts += 1
                preflight_ok, preflight_msg = self.preflight_check(profile)
                if not preflight_ok:
                    if on_output:
                        on_output(preflight_msg)
                    self._record_history(
                        profile,
                        command_set,
                        result="failed",
                        error_code="preflight_failed",
                        error_message=preflight_msg,
                        wlog_path=None,
                    )
                    last_result = LaunchResult("failed", "preflight_failed", Path(""), attempts)
                    break
                try:
                    last_result = self._launch_once(
                        profile,
                        command_set,
                        password,
                        cancel_event,
                        on_output,
                        timeout_s,
                        attempt=attempts,
                    )
                except TimeoutError:
                    last_result = LaunchResult("failed", "timeout", Path(""), attempts)
                except Exception:
                    last_result = LaunchResult("failed", "launch_failed", Path(""), attempts)
                if last_result.error_code is None or last_result.result == "success":
                    break
                if attempts <= max_retries and on_output:
                    on_output(f"Reconnect attempt {attempts} failed ({last_result.error_code}); retrying...")
                time.sleep(0.2)
            if last_result:
                on_complete(last_result)

        thread = threading.Thread(target=runner, daemon=True)
        thread.start()
        return LaunchSession(thread=thread, cancel_event=cancel_event, timeout_s=timeout_s)

    def _launch_once(
        self,
        profile: Profile,
        command_set: CommandSet,
        password: Optional[str],
        cancel_event: threading.Event,
        on_output: Optional[Callable[[str], None]],
        timeout_s: float,
        *,
        attempt: int,
    ) -> LaunchResult:
        ttl_file: Optional[Path] = None
        wlog_path: Optional[Path] = None
        start = time.monotonic()
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
                self._run_stub_stream(
                    profile,
                    command_set,
                    password,
                    ttl_file,
                    wlog_path,
                    cancel_event,
                    on_output,
                    start,
                    timeout_s,
                    attempt,
                )
            else:
                raise NotImplementedError("Real Tera Term execution not implemented in this environment")
            error_code = self._analyze_wlog(wlog_path)
            result = "success" if error_code is None else "failed"
        except TimeoutError:
            error_code = "timeout"
            result = "failed"
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
            error_message=f"attempt {attempt}" if attempt > 1 else error_code,
            wlog_path=wlog_path,
        )
        return LaunchResult(result=result, error_code=error_code, wlog_path=wlog_path or Path(""), attempts=attempt)

    def _write_ttl(self, content: str) -> Path:
        fd, path_str = tempfile.mkstemp(prefix="tt-launch-", suffix=".ttl")
        os.close(fd)
        ttl_file = Path(path_str)
        ttl_file.write_text(content, encoding="utf-8")
        return ttl_file

    def _run_stub_stream(
        self,
        profile: Profile,
        command_set: CommandSet,
        password: Optional[str],
        ttl_file: Path,
        wlog: Path,
        cancel_event: threading.Event,
        on_output: Optional[Callable[[str], None]],
        start: float,
        timeout_s: float,
        attempt: int,
    ) -> None:
        lines = [
            f"Connecting to {profile.host}:{profile.port} as {profile.user}",
            "Using stub mode - not invoking Tera Term",
            f"TTL file: {ttl_file}",
        ]
        failing = profile.auth_type == "password" and not password or password == "bad" or profile.host.startswith(
            "invalid"
        )
        flaky = profile.host.startswith("flaky")
        if failing and not flaky:
            lines.append("Login failed")
        else:
            if flaky and attempt == 1:
                lines.append("Login failed")
            else:
                lines.append("Login successful")
                for cmd in command_set.commands:
                    lines.append(f"RUN: {cmd}")
                lines.append("OK_FROM_SERVER")
        output: list[str] = []
        for line in lines:
            if cancel_event.is_set():
                output.append("Cancelled")
                break
            if time.monotonic() - start > timeout_s:
                raise TimeoutError("Launch exceeded timeout")
            output.append(line)
            if on_output:
                on_output(line)
            time.sleep(0.05)
        wlog.write_text("\n".join(output), encoding="utf-8")

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

    def _default_preflight(self, profile: Profile) -> tuple[bool, str]:
        try:
            socket.getaddrinfo(profile.host, profile.port)
            with socket.create_connection((profile.host, profile.port), timeout=1) as sock:
                sock.settimeout(1)
            return True, "Preflight OK"
        except Exception as exc:
            return False, f"Preflight failed: {exc}"


__all__ = ["LaunchResult", "Launcher"]
