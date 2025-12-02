"""Credential management with fallback to restricted mode."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import string
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

import keyring


@dataclass
class Credential:
    """Represents a stored credential payload."""

    username: Optional[str]
    secret: str


class CredentialStore:
    """Wrapper around keyring with health checks and restricted fallback."""

    def __init__(self, app_id: str = "tt-launcher", app_dir: Optional[Path] = None) -> None:
        self.app_id = app_id
        self.app_dir = app_dir or Path.home() / ".forteraterm"
        self.app_dir.mkdir(parents=True, exist_ok=True)
        self._mode = self._detect_mode()
        self._master_key: bytes | None = None

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def restricted(self) -> bool:
        return self._mode == "restricted"

    def _detect_mode(self) -> str:
        backend = keyring.get_keyring()
        # Try a quick round-trip to validate the backend actually works.
        probe_ref = "cred:healthcheck"
        probe_secret = self._generate_secret()
        try:
            keyring.set_password(self.app_id, probe_ref, probe_secret)
            fetched = keyring.get_password(self.app_id, probe_ref)
            keyring.delete_password(self.app_id, probe_ref)
        except Exception:
            return self._detect_local_mode()
        if fetched != probe_secret:
            return self._detect_local_mode()
        # Prefer Credential Manager on Windows but allow anything that passes the round-trip.
        if backend.name and "credential" in backend.name.lower():
            return "standard"
        return "standard"

    def _detect_local_mode(self) -> str:
        try:
            self._ensure_local_key()
        except Exception:
            return "restricted"
        return "local_encrypted"

    def _ensure_local_key(self) -> None:
        key_path = self.app_dir / "master.key"
        if key_path.exists():
            return
        key = secrets.token_bytes(32)
        key_path.write_bytes(key)
        try:
            os.chmod(key_path, 0o600)
        except OSError:
            # Best effort; some platforms ignore chmod on files.
            pass

    def _load_master_key(self) -> bytes:
        if self._master_key:
            return self._master_key
        key_path = self.app_dir / "master.key"
        if not key_path.exists():
            self._ensure_local_key()
        self._master_key = key_path.read_bytes()
        return self._master_key

    def _load_local_store(self) -> Dict[str, dict]:
        creds_path = self.app_dir / "creds.json"
        if not creds_path.exists():
            return {}
        try:
            return json.loads(creds_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            raise RuntimeError("Local credential store is corrupted; delete creds.json to regenerate")

    def _load_local_store_plaintext(self) -> Dict[str, dict]:
        data = self._load_local_store()
        plaintext: Dict[str, dict] = {}
        for ref, payload in data.items():
            plaintext[ref] = {
                "username": payload.get("username"),
                "secret": self._decrypt_secret(payload.get("secret", "")),
            }
        return plaintext

    def _save_local_store(self, data: Dict[str, dict]) -> None:
        creds_path = self.app_dir / "creds.json"
        creds_path.write_text(json.dumps(data), encoding="utf-8")

    def _save_local_plaintext(self, data: Dict[str, dict]) -> None:
        encrypted: Dict[str, dict] = {}
        for ref, payload in data.items():
            encrypted[ref] = {
                "username": payload.get("username"),
                "secret": self._encrypt_secret(payload.get("secret", "")),
            }
        self._save_local_store(encrypted)

    def register(self, label: str, username: Optional[str], secret: str) -> str:
        cred_ref = f"cred:{self._slugify(label)}"
        if self._mode == "restricted":
            raise RuntimeError("Credential storage unavailable in restricted mode")
        if self._mode == "standard":
            payload = json.dumps({"username": username, "secret": secret})
            keyring.set_password(self.app_id, cred_ref, payload)
            return cred_ref
        encrypted = self._encrypt_secret(secret)
        data = self._load_local_store()
        data[cred_ref] = {"username": username, "secret": encrypted}
        self._save_local_store(data)
        return cred_ref

    def get(self, cred_ref: str) -> Optional[Credential]:
        if self._mode == "restricted":
            return None
        if self._mode == "standard":
            payload = keyring.get_password(self.app_id, cred_ref)
            if payload is None:
                return None
            try:
                parsed = json.loads(payload)
            except json.JSONDecodeError:
                return None
            return Credential(username=parsed.get("username"), secret=parsed.get("secret", ""))
        data = self._load_local_store()
        stored = data.get(cred_ref)
        if not stored:
            return None
        secret = self._decrypt_secret(stored.get("secret", ""))
        return Credential(username=stored.get("username"), secret=secret)

    def update(self, cred_ref: str, username: Optional[str], secret: str) -> None:
        if self._mode == "restricted":
            raise RuntimeError("Credential storage unavailable in restricted mode")
        if self._mode == "standard":
            payload = json.dumps({"username": username, "secret": secret})
            keyring.set_password(self.app_id, cred_ref, payload)
            return
        data = self._load_local_store()
        data[cred_ref] = {"username": username, "secret": self._encrypt_secret(secret)}
        self._save_local_store(data)

    def delete(self, cred_ref: str) -> None:
        if self._mode == "restricted":
            raise RuntimeError("Credential storage unavailable in restricted mode")
        if self._mode == "standard":
            keyring.delete_password(self.app_id, cred_ref)
            return
        data = self._load_local_store()
        data.pop(cred_ref, None)
        self._save_local_store(data)

    def rotate_keys(self) -> None:
        if self._mode != "local_encrypted":
            raise RuntimeError("Key rotation only applies to local encrypted mode")
        plaintext = self._load_local_store_plaintext()
        key_path = self.app_dir / "master.key"
        backup_path = self.app_dir / "master.key.bak"
        if key_path.exists():
            key_path.replace(backup_path)
        self._master_key = None
        self._ensure_local_key()
        self._save_local_plaintext(plaintext)

    def export_encrypted(self, export_path: Path, password: str) -> None:
        if self._mode != "local_encrypted":
            raise RuntimeError("Encrypted export requires local encrypted mode")
        plaintext = self._load_local_store_plaintext()
        blob = json.dumps(plaintext).encode("utf-8")
        salt = secrets.token_bytes(16)
        key = self._derive_password_key(password, salt)
        cipher = self._xor_keystream(blob, key)
        mac = hmac.new(key, blob, hashlib.sha256).digest()
        payload = {
            "version": 1,
            "salt": base64.urlsafe_b64encode(salt).decode("utf-8"),
            "cipher": base64.urlsafe_b64encode(cipher).decode("utf-8"),
            "hmac": base64.urlsafe_b64encode(mac).decode("utf-8"),
        }
        export_path.parent.mkdir(parents=True, exist_ok=True)
        export_path.write_text(json.dumps(payload), encoding="utf-8")

    def import_encrypted(self, import_path: Path, password: str) -> None:
        if self._mode != "local_encrypted":
            raise RuntimeError("Encrypted import requires local encrypted mode")
        payload = json.loads(import_path.read_text(encoding="utf-8"))
        if payload.get("version") != 1:
            raise RuntimeError("Unsupported export version")
        salt = base64.urlsafe_b64decode(payload["salt"])
        cipher = base64.urlsafe_b64decode(payload["cipher"])
        mac = base64.urlsafe_b64decode(payload["hmac"])
        key = self._derive_password_key(password, salt)
        plaintext = self._xor_keystream(cipher, key)
        if not hmac.compare_digest(mac, hmac.new(key, plaintext, hashlib.sha256).digest()):
            raise RuntimeError("Integrity check failed; wrong password or corrupted file")
        data = json.loads(plaintext.decode("utf-8"))
        self._save_local_plaintext(data)

    def _generate_secret(self, length: int = 24) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def _slugify(self, value: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
        if not slug:
            slug = self._generate_secret(6)
        return slug

    def _encrypt_secret(self, plaintext: str) -> str:
        key = self._load_master_key()
        salt = secrets.token_bytes(16)
        stream_key = hashlib.sha256(key + salt).digest()
        data = plaintext.encode("utf-8")
        keystream = bytearray()
        counter = 0
        while len(keystream) < len(data):
            block = hmac.new(stream_key, counter.to_bytes(4, "big"), hashlib.sha256).digest()
            keystream.extend(block)
            counter += 1
        cipher = bytes(a ^ b for a, b in zip(data, keystream))
        return base64.urlsafe_b64encode(salt + cipher).decode("utf-8")

    def _decrypt_secret(self, encoded: str) -> str:
        try:
            blob = base64.urlsafe_b64decode(encoded.encode("utf-8"))
        except Exception as exc:  # pragma: no cover - defensive path
            raise RuntimeError("Failed to decode stored credential payload") from exc
        if len(blob) < 17:
            raise RuntimeError("Stored credential payload is invalid")
        salt, cipher = blob[:16], blob[16:]
        key = self._load_master_key()
        stream_key = hashlib.sha256(key + salt).digest()
        keystream = bytearray()
        counter = 0
        while len(keystream) < len(cipher):
            block = hmac.new(stream_key, counter.to_bytes(4, "big"), hashlib.sha256).digest()
            keystream.extend(block)
            counter += 1
        plaintext = bytes(a ^ b for a, b in zip(cipher, keystream[: len(cipher)])).decode("utf-8")
        return plaintext

    def _derive_password_key(self, password: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000, dklen=32)

    def _xor_keystream(self, data: bytes, key: bytes) -> bytes:
        keystream = bytearray()
        counter = 0
        while len(keystream) < len(data):
            block = hmac.new(key, counter.to_bytes(4, "big"), hashlib.sha256).digest()
            keystream.extend(block)
            counter += 1
        return bytes(a ^ b for a, b in zip(data, keystream))


__all__ = ["Credential", "CredentialStore"]
