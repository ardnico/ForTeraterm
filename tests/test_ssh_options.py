from ForTeraterm.ssh_options import PortForward, add_keepalive_options, build_ssh_options, parse_ssh_options


def test_parse_and_build_roundtrip() -> None:
    forwards, extras = parse_ssh_options("/FWD=2222=localhost:22 /FWD=8080=svc:80 -v")
    assert len(forwards) == 2
    assert extras == "-v"
    rebuilt = build_ssh_options(forwards, extras)
    assert rebuilt == "/FWD=2222=localhost:22 /FWD=8080=svc:80 -v"


def test_parse_with_invalid_tokens_keeps_extras() -> None:
    forwards, extras = parse_ssh_options("/FWD=badtoken other")
    assert forwards == []
    assert extras == "/FWD=badtoken other"


def test_build_skips_incomplete_entries() -> None:
    forwards = [PortForward(local_port="", remote_host="", remote_port=""), PortForward("9000", "app", "9000")]
    assert build_ssh_options(forwards, "") == "/FWD=9000=app:9000"


def test_add_keepalive_options() -> None:
    base = "/FWD=2222=localhost:22"
    keepalive = add_keepalive_options(base, interval=10, count=2)
    assert "ServerAliveInterval=10" in keepalive
    assert "ServerAliveCountMax=2" in keepalive
    standalone = add_keepalive_options("")
    assert standalone.startswith("-o ServerAliveInterval")
