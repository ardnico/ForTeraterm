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
        ssh_options="",
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


def test_empty_commands_allowed(tmp_path: Path) -> None:
    cs = sample_command_set()
    cs.commands = []
    ttl = renderer(tmp_path).render(sample_profile(), cs, password="secret")
    assert "sendln" not in ttl.lower()


def test_password_and_command_are_escaped(tmp_path: Path) -> None:
    cs = sample_command_set()
    cs.commands = ['echo "hello"']
    ttl = renderer(tmp_path).render(sample_profile(), cs, password='p"ass')
    assert '/passwd=\\"p""ass\\"' in ttl
    assert 'sendln "echo ""hello"""' in ttl


def test_ssh_options_are_included(tmp_path: Path) -> None:
    cs = sample_command_set()
    profile = sample_profile()
    profile.ssh_options = "/FWD=2222=localhost:22 /FWD=3333=localhost:33"
    ttl = renderer(tmp_path).render(profile, cs, password=None)
    assert "/auth=password /fwd=2222=localhost:22 /fwd=3333=localhost:33" in ttl.lower()
