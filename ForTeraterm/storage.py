"""Data storage layer for TeraTerm Connection Launcher (v3).

This module owns the SQLite schema and offers convenience helpers for
storing profiles, command sets, and connection history records.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


SCHEMA_VERSION = 1


@dataclass
class CommandSet:
    """Represents a reusable set of commands to run after login."""

    id: Optional[int]
    ref_id: str
    label: str
    description: str
    commands: List[str]


@dataclass
class Profile:
    """Represents a single connection target and its configuration."""

    id: Optional[int]
    name: str
    host: str
    port: int
    user: str
    auth_type: str
    cred_ref: Optional[str]
    ttl_template_version: str
    command_set_id: int


@dataclass
class HistoryRecord:
    """Represents a historical connection attempt."""

    id: Optional[int]
    profile_id: int
    command_set_id: Optional[int]
    connected_at: str
    result: str
    error_code: Optional[str]
    error_message_short: Optional[str]
    ttl_template_version: str
    wlog_path: Optional[str]


class DataStore:
    """High-level interface for the SQLite database."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        cur = self._conn.cursor()
        cur.execute("PRAGMA user_version")
        current_version = cur.fetchone()[0]
        if current_version == 0:
            self._create_schema()
            self._conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
            self._conn.commit()
        elif current_version != SCHEMA_VERSION:
            raise RuntimeError(
                f"Unsupported schema version {current_version}; expected {SCHEMA_VERSION}."
            )

    def _create_schema(self) -> None:
        cur = self._conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS command_sets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ref_id TEXT UNIQUE NOT NULL,
                label TEXT NOT NULL,
                description TEXT,
                commands TEXT NOT NULL
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER NOT NULL,
                user TEXT NOT NULL,
                auth_type TEXT NOT NULL,
                cred_ref TEXT,
                ttl_template_version TEXT NOT NULL,
                command_set_id INTEGER NOT NULL,
                FOREIGN KEY(command_set_id) REFERENCES command_sets(id)
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                command_set_id INTEGER,
                connected_at TEXT NOT NULL,
                result TEXT NOT NULL,
                error_code TEXT,
                error_message_short TEXT,
                ttl_template_version TEXT NOT NULL,
                wlog_path TEXT,
                FOREIGN KEY(profile_id) REFERENCES profiles(id),
                FOREIGN KEY(command_set_id) REFERENCES command_sets(id)
            );
            """
        )
        self._conn.commit()

    # ---------- Command sets ----------
    def upsert_command_set(self, command_set: CommandSet) -> int:
        commands_json = json.dumps(command_set.commands)
        cur = self._conn.cursor()
        if command_set.id is None:
            cur.execute(
                """
                INSERT INTO command_sets (ref_id, label, description, commands)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(ref_id) DO UPDATE SET
                    label=excluded.label,
                    description=excluded.description,
                    commands=excluded.commands
                RETURNING id;
                """,
                (command_set.ref_id, command_set.label, command_set.description, commands_json),
            )
        else:
            cur.execute(
                """
                UPDATE command_sets
                   SET ref_id=?, label=?, description=?, commands=?
                 WHERE id=?
                RETURNING id;
                """,
                (
                    command_set.ref_id,
                    command_set.label,
                    command_set.description,
                    commands_json,
                    command_set.id,
                ),
            )
        new_id = cur.fetchone()[0]
        self._conn.commit()
        return int(new_id)

    def get_command_set(self, command_set_id: int) -> CommandSet:
        cur = self._conn.execute(
            "SELECT id, ref_id, label, description, commands FROM command_sets WHERE id=?",
            (command_set_id,),
        )
        row = cur.fetchone()
        if row is None:
            raise KeyError(f"Command set {command_set_id} not found")
        return CommandSet(
            id=row["id"],
            ref_id=row["ref_id"],
            label=row["label"],
            description=row["description"],
            commands=json.loads(row["commands"]),
        )

    def find_command_set_by_ref(self, ref_id: str) -> Optional[CommandSet]:
        cur = self._conn.execute(
            "SELECT id, ref_id, label, description, commands FROM command_sets WHERE ref_id=?",
            (ref_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return CommandSet(
            id=row["id"],
            ref_id=row["ref_id"],
            label=row["label"],
            description=row["description"],
            commands=json.loads(row["commands"]),
        )

    # ---------- Profiles ----------
    def upsert_profile(self, profile: Profile) -> int:
        cur = self._conn.cursor()
        if profile.id is None:
            cur.execute(
                """
                INSERT INTO profiles
                    (name, host, port, user, auth_type, cred_ref, ttl_template_version, command_set_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                RETURNING id;
                """,
                (
                    profile.name,
                    profile.host,
                    profile.port,
                    profile.user,
                    profile.auth_type,
                    profile.cred_ref,
                    profile.ttl_template_version,
                    profile.command_set_id,
                ),
            )
        else:
            cur.execute(
                """
                UPDATE profiles
                   SET name=?, host=?, port=?, user=?, auth_type=?, cred_ref=?, ttl_template_version=?, command_set_id=?
                 WHERE id=?
                RETURNING id;
                """,
                (
                    profile.name,
                    profile.host,
                    profile.port,
                    profile.user,
                    profile.auth_type,
                    profile.cred_ref,
                    profile.ttl_template_version,
                    profile.command_set_id,
                    profile.id,
                ),
            )
        new_id = cur.fetchone()[0]
        self._conn.commit()
        return int(new_id)

    def list_profiles(self) -> List[Profile]:
        cur = self._conn.execute(
            "SELECT id, name, host, port, user, auth_type, cred_ref, ttl_template_version, command_set_id FROM profiles ORDER BY name"
        )
        rows = cur.fetchall()
        return [
            Profile(
                id=row["id"],
                name=row["name"],
                host=row["host"],
                port=row["port"],
                user=row["user"],
                auth_type=row["auth_type"],
                cred_ref=row["cred_ref"],
                ttl_template_version=row["ttl_template_version"],
                command_set_id=row["command_set_id"],
            )
            for row in rows
        ]

    def get_profile(self, profile_id: int) -> Profile:
        cur = self._conn.execute(
            "SELECT id, name, host, port, user, auth_type, cred_ref, ttl_template_version, command_set_id FROM profiles WHERE id=?",
            (profile_id,),
        )
        row = cur.fetchone()
        if row is None:
            raise KeyError(f"Profile {profile_id} not found")
        return Profile(
            id=row["id"],
            name=row["name"],
            host=row["host"],
            port=row["port"],
            user=row["user"],
            auth_type=row["auth_type"],
            cred_ref=row["cred_ref"],
            ttl_template_version=row["ttl_template_version"],
            command_set_id=row["command_set_id"],
        )

    # ---------- History ----------
    def record_history(self, record: HistoryRecord) -> int:
        cur = self._conn.cursor()
        cur.execute(
            """
            INSERT INTO history (profile_id, command_set_id, connected_at, result, error_code, error_message_short, ttl_template_version, wlog_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id;
            """,
            (
                record.profile_id,
                record.command_set_id,
                record.connected_at,
                record.result,
                record.error_code,
                record.error_message_short,
                record.ttl_template_version,
                record.wlog_path,
            ),
        )
        new_id = cur.fetchone()[0]
        self._conn.commit()
        return int(new_id)

    def list_history_for_profile(self, profile_id: int, limit: int = 50) -> List[HistoryRecord]:
        cur = self._conn.execute(
            """
            SELECT id, profile_id, command_set_id, connected_at, result, error_code, error_message_short, ttl_template_version, wlog_path
              FROM history
             WHERE profile_id=?
             ORDER BY datetime(connected_at) DESC
             LIMIT ?
            """,
            (profile_id, limit),
        )
        rows = cur.fetchall()
        return [
            HistoryRecord(
                id=row["id"],
                profile_id=row["profile_id"],
                command_set_id=row["command_set_id"],
                connected_at=row["connected_at"],
                result=row["result"],
                error_code=row["error_code"],
                error_message_short=row["error_message_short"],
                ttl_template_version=row["ttl_template_version"],
                wlog_path=row["wlog_path"],
            )
            for row in rows
        ]

    # ---------- Export / Import ----------
    def export_data(self) -> dict:
        profiles = self.list_profiles()
        cmd_sets = self._conn.execute(
            "SELECT id, ref_id, label, description, commands FROM command_sets"
        ).fetchall()
        return {
            "schema_version": SCHEMA_VERSION,
            "profiles": [
                {
                    "id": profile.id,
                    "name": profile.name,
                    "host": profile.host,
                    "port": profile.port,
                    "user": profile.user,
                    "auth_type": profile.auth_type,
                    "cred_ref": profile.cred_ref,
                    "ttl_template_version": profile.ttl_template_version,
                    "command_set_id": self.get_command_set(profile.command_set_id).ref_id,
                }
                for profile in profiles
            ],
            "command_sets": [
                {
                    "id": row["ref_id"],
                    "label": row["label"],
                    "description": row["description"],
                    "commands": json.loads(row["commands"]),
                }
                for row in cmd_sets
            ],
        }

    def import_data(self, data: dict) -> None:
        if data.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(
                f"Unsupported schema_version {data.get('schema_version')}; expected {SCHEMA_VERSION}."
            )
        ref_to_id: dict[str, int] = {}
        for cmd_set in data.get("command_sets", []):
            cs = CommandSet(
                id=None,
                ref_id=cmd_set["id"],
                label=cmd_set.get("label", cmd_set["id"]),
                description=cmd_set.get("description", ""),
                commands=cmd_set.get("commands", []),
            )
            ref_to_id[cs.ref_id] = self.upsert_command_set(cs)
        for profile in data.get("profiles", []):
            ref_id = profile.get("command_set_id")
            if ref_id not in ref_to_id:
                raise ValueError(f"Command set {ref_id} referenced by profile is missing")
            new_profile = Profile(
                id=None,
                name=profile["name"],
                host=profile["host"],
                port=int(profile.get("port", 22)),
                user=profile["user"],
                auth_type=profile.get("auth_type", "password"),
                cred_ref=profile.get("cred_ref"),
                ttl_template_version=profile.get("ttl_template_version", "v1-basic"),
                command_set_id=ref_to_id[ref_id],
            )
            self.upsert_profile(new_profile)

    def close(self) -> None:
        self._conn.close()


__all__ = [
    "CommandSet",
    "DataStore",
    "HistoryRecord",
    "Profile",
    "SCHEMA_VERSION",
]
