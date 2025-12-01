import os
import tempfile
from pathlib import Path

import pytest

from ForTeraterm.launcher import Launcher
from ForTeraterm.storage import DataStore
from ForTeraterm.ttl_renderer import TTLRenderer


@pytest.fixture
def launcher(tmp_path: Path) -> Launcher:
    renderer = TTLRenderer(Path(__file__).parents[1] / "templates")
    storage = DataStore(tmp_path / "db.sqlite")
    launcher = Launcher(renderer, storage, stub_mode=True)
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
