"""Minimal local keyring stub used for offline testing.

This is **not** a drop-in replacement for the real `keyring` package but
provides enough of the API for this project and its tests.
"""

from __future__ import annotations

from typing import Optional

from .backend import KeyringBackend

__all__ = [
    "KeyringBackend",
    "get_keyring",
    "set_keyring",
    "set_password",
    "get_password",
    "delete_password",
]


class InMemoryKeyring(KeyringBackend):
    name = "InMemoryKeyring"
    priority = 1

    def __init__(self) -> None:
        self.store: dict[tuple[str, str], str] = {}

    def get_password(self, service: str, username: str) -> Optional[str]:
        return self.store.get((service, username))

    def set_password(self, service: str, username: str, password: str) -> None:
        self.store[(service, username)] = password

    def delete_password(self, service: str, username: str) -> None:
        self.store.pop((service, username), None)


_keyring: KeyringBackend = InMemoryKeyring()
__version__ = "0.0-stub"


def get_keyring() -> KeyringBackend:
    return _keyring


def set_keyring(keyring_backend: KeyringBackend) -> None:
    global _keyring
    _keyring = keyring_backend


def set_password(service: str, username: str, password: str) -> None:
    _keyring.set_password(service, username, password)


def get_password(service: str, username: str) -> Optional[str]:
    return _keyring.get_password(service, username)


def delete_password(service: str, username: str) -> None:
    _keyring.delete_password(service, username)
