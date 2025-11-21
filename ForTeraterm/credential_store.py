"""Credential management with fallback to restricted mode."""

from __future__ import annotations

import json
import re
import secrets
import string
from dataclasses import dataclass
from typing import Optional

import keyring


@dataclass
class Credential:
    """Represents a stored credential payload."""

    username: Optional[str]
    secret: str


class CredentialStore:
    """Wrapper around keyring with health checks and restricted fallback."""

    def __init__(self, app_id: str = "tt-launcher") -> None:
        self.app_id = app_id
        self._mode = self._detect_mode()

    @property
    def mode(self) -> str:
        return "restricted" if self._mode == "restricted" else "standard"

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
            return "restricted"
        if fetched != probe_secret:
            return "restricted"
        # Prefer Credential Manager on Windows but allow anything that passes the round-trip.
        if backend.name and "credential" in backend.name.lower():
            return "standard"
        return "standard"

    def register(self, label: str, username: Optional[str], secret: str) -> str:
        if self.restricted:
            raise RuntimeError("Credential storage unavailable in restricted mode")
        cred_ref = f"cred:{self._slugify(label)}"
        payload = json.dumps({"username": username, "secret": secret})
        keyring.set_password(self.app_id, cred_ref, payload)
        return cred_ref

    def get(self, cred_ref: str) -> Optional[Credential]:
        if self.restricted:
            return None
        payload = keyring.get_password(self.app_id, cred_ref)
        if payload is None:
            return None
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError:
            return None
        return Credential(username=parsed.get("username"), secret=parsed.get("secret", ""))

    def update(self, cred_ref: str, username: Optional[str], secret: str) -> None:
        if self.restricted:
            raise RuntimeError("Credential storage unavailable in restricted mode")
        payload = json.dumps({"username": username, "secret": secret})
        keyring.set_password(self.app_id, cred_ref, payload)

    def delete(self, cred_ref: str) -> None:
        if self.restricted:
            raise RuntimeError("Credential storage unavailable in restricted mode")
        keyring.delete_password(self.app_id, cred_ref)

    def _generate_secret(self, length: int = 24) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def _slugify(self, value: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
        if not slug:
            slug = self._generate_secret(6)
        return slug


__all__ = ["Credential", "CredentialStore"]
