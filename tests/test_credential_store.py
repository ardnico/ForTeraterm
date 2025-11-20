import keyring
from keyring.backend import KeyringBackend

from ForTeraterm.credential_store import CredentialStore


class MemoryKeyring(KeyringBackend):
    priority = 1

    def __init__(self) -> None:
        self.store: dict[tuple[str, str], str] = {}

    def get_password(self, service: str, username: str) -> str | None:
        return self.store.get((service, username))

    def set_password(self, service: str, username: str, password: str) -> None:
        self.store[(service, username)] = password

    def delete_password(self, service: str, username: str) -> None:
        self.store.pop((service, username), None)


def test_standard_mode_with_memory_keyring(monkeypatch) -> None:
    keyring.set_keyring(MemoryKeyring())
    store = CredentialStore(app_id="test-launcher")
    assert store.mode == "standard"
    cred_ref = store.register("demo", "alice", "s3cret")
    retrieved = store.get(cred_ref)
    assert retrieved is not None
    assert retrieved.secret == "s3cret"
    assert retrieved.username == "alice"
