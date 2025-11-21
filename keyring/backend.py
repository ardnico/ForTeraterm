"""Backend base class for the local keyring stub."""

from __future__ import annotations

from typing import Optional


class KeyringBackend:
    name = "KeyringBackend"
    priority = 0

    def get_password(self, service: str, username: str) -> Optional[str]:
        raise NotImplementedError

    def set_password(self, service: str, username: str, password: str) -> None:
        raise NotImplementedError

    def delete_password(self, service: str, username: str) -> None:
        raise NotImplementedError
