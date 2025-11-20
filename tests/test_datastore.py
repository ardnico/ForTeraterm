from pathlib import Path

from ForTeraterm.storage import CommandSet, DataStore, HistoryRecord, Profile


def test_profile_and_history_roundtrip(tmp_path: Path) -> None:
    db = DataStore(tmp_path / "test.db")
    cmd_set = CommandSet(id=None, ref_id="cmd:test", label="Test", description="", commands=["echo ok"])
    cmd_id = db.upsert_command_set(cmd_set)
    profile = Profile(
        id=None,
        name="demo",
        host="example.com",
        port=22,
        user="deploy",
        auth_type="password",
        cred_ref=None,
        ttl_template_version="v1-basic",
        command_set_id=cmd_id,
    )
    profile_id = db.upsert_profile(profile)
    record = HistoryRecord(
        id=None,
        profile_id=profile_id,
        command_set_id=cmd_id,
        connected_at="2024-01-01T00:00:00",
        result="success",
        error_code=None,
        error_message_short=None,
        ttl_template_version="v1-basic",
        wlog_path="/tmp/wlog",
    )
    db.record_history(record)

    profiles = db.list_profiles()
    assert len(profiles) == 1
    history = db.list_history_for_profile(profile_id)
    assert len(history) == 1
    exported = db.export_data()
    assert exported["schema_version"] == 1
    db.close()
