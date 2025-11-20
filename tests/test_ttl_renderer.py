from pathlib import Path

import pytest

from ForTeraterm.storage import CommandSet, Profile
from ForTeraterm.ttl_renderer import TTLRenderer


def renderer(tmp_path: Path) -> TTLRenderer:
    template_root = Path(__file__).parents[1] / "templates"
    return TTLRenderer(template_root)


def sample_profile() -> Profile:
    return Profile(
        id=1,
        name="demo",
        host="example.com",
        port=22,
        user="deploy",
        auth_type="password",
        cred_ref=None,
        ttl_template_version="v1-basic",
        command_set_id=1,
    )


def sample_command_set() -> CommandSet:
    return CommandSet(
        id=1,
        ref_id="cmd:demo",
        label="Demo",
        description="",
        commands=["echo ok"],
    )


def test_render_outputs_connect_and_end(tmp_path: Path) -> None:
    ttl = renderer(tmp_path).render(sample_profile(), sample_command_set(), password="secret")
    assert "connect" in ttl
    assert ttl.strip().lower().endswith("end")


def test_invalid_command_with_newline_raises(tmp_path: Path) -> None:
    cs = sample_command_set()
    cs.commands = ["bad\ncommand"]
    with pytest.raises(ValueError):
        renderer(tmp_path).render(sample_profile(), cs, password="secret")
