from pathlib import Path

from ForTeraterm.storage import AppSettings, CommandSet, DataStore, HistoryRecord, Profile


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
        ssh_options="",
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
    history = db.list_history_for_profile(profile_id, result_filter="success")
    assert len(history) == 1
    filtered = db.list_history_for_profile(profile_id, result_filter="failed")
    assert filtered == []
    exported = db.export_data()
    assert exported["schema_version"] == 3
    assert exported["profiles"][0]["command_set_ids"] == ["cmd:test"]
    assert "exported_at" in exported
    assert db.list_command_sets()
    db.close()


def test_settings_defaults_and_persistence(tmp_path: Path) -> None:
    db_path = tmp_path / "settings.db"
    first = DataStore(db_path)
    defaults = first.load_settings()
    assert defaults.appearance_mode == "system"
    assert defaults.color_theme == "blue"
    assert defaults.font_family == "Arial"
    assert defaults.font_size == 12

    new_settings = AppSettings(
        appearance_mode="dark",
        color_theme="green",
        font_family="Consolas",
        font_size=14,
    )
    first.save_settings(new_settings)
    first.close()

    reloaded = DataStore(db_path).load_settings()
    assert reloaded == new_settings
