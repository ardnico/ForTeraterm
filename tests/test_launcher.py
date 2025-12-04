import os
import tempfile
import threading
from pathlib import Path

import pytest

from ForTeraterm.launcher import Launcher
from ForTeraterm.storage import CommandSet, DataStore, Profile
from ForTeraterm.ttl_renderer import TTLRenderer


@pytest.fixture
def launcher(tmp_path: Path) -> Launcher:
    renderer = TTLRenderer(Path(__file__).parents[1] / "templates")
    storage = DataStore(tmp_path / "db.sqlite")
    launcher = Launcher(renderer, storage, stub_mode=True, preflight_check=lambda _p: (True, "ok"))
    yield launcher
    storage.close()


def test_write_ttl_closes_tempfile_handle(monkeypatch: pytest.MonkeyPatch, launcher: Launcher, tmp_path: Path) -> None:
    recorded: dict[str, int] = {}
    temp_path = tmp_path / "locked.ttl"

    def fake_mkstemp(prefix: str, suffix: str):
        fd = os.open(temp_path, os.O_CREAT | os.O_RDWR)
        recorded["fd"] = fd
        return fd, str(temp_path)

    monkeypatch.setattr(tempfile, "mkstemp", fake_mkstemp)

    ttl_path = launcher._write_ttl("sample")
    assert ttl_path == temp_path

    with pytest.raises(OSError):
        os.close(recorded["fd"])


def _create_profile_and_commands(storage: DataStore) -> tuple[Profile, CommandSet]:
    cmd_set = CommandSet(id=None, ref_id="cmd:test", label="Test", description="", commands=["echo ok"])
    cmd_id = storage.upsert_command_set(cmd_set)
    profile = Profile(
        id=None,
        name="demo",
        host="example.com",
        port=22,
        user="deploy",
        auth_type="password",
        cred_ref=None,
        ssh_options="",
        ttl_template_version="v1-basic",
        command_set_id=cmd_id,
        tags=[],
    )
    profile_id = storage.upsert_profile(profile)
    profile.id = profile_id
    cmd_set.id = cmd_id
    return profile, cmd_set


def test_async_launch_streams_and_records(tmp_path: Path) -> None:
    renderer = TTLRenderer(Path(__file__).parents[1] / "templates")
    storage = DataStore(tmp_path / "db.sqlite")
    launcher = Launcher(renderer, storage, stub_mode=True, preflight_check=lambda _p: (True, "ok"))
    profile, cmd_set = _create_profile_and_commands(storage)
    lines: list[str] = []
    done = threading.Event()
    results: list = []

    def on_output(line: str) -> None:
        lines.append(line)

    def on_complete(res) -> None:
        results.append(res)
        done.set()

    launcher.launch_async(profile, cmd_set, None, "secret", on_output=on_output, on_complete=on_complete, max_retries=0)
    done.wait(timeout=5)
    assert lines
    assert results
    history = storage.list_history_for_profile(profile.id or 0)
    assert history
    assert history[0].result in {"success", "failed"}
    storage.close()


def test_auto_reconnect_on_flaky_host(tmp_path: Path) -> None:
    renderer = TTLRenderer(Path(__file__).parents[1] / "templates")
    storage = DataStore(tmp_path / "db.sqlite")
    launcher = Launcher(renderer, storage, stub_mode=True, preflight_check=lambda _p: (True, "ok"))
    profile, cmd_set = _create_profile_and_commands(storage)
    profile.host = "flaky.example"
    lines: list[str] = []
    done = threading.Event()
    results: list = []

    launcher.launch_async(profile, cmd_set, None, "secret", on_output=lines.append, on_complete=lambda r: (results.append(r), done.set()), max_retries=1)
    done.wait(timeout=5)
    assert results
    assert results[0].attempts >= 1
    history = storage.list_history_for_profile(profile.id or 0)
    assert history
    storage.close()
