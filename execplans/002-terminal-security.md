# Surface terminal, editing, and secure credentials

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds. Maintain this document in accordance with `.agent/PLANS.md`.

## Purpose / Big Picture

Operators need to see terminal output when launching sessions, adjust saved connection settings later, manage flexible SSH port forwards, inspect server configuration details, and store connection passwords securely even when a system keyring is unavailable. After this change, connecting to a server will surface a terminal-style log window, profiles can be edited (including port forwards), multiple SSH forwards can be configured easily, selected servers show rich details, and encrypted password storage works without depending solely on the OS keyring.

## Progress

- [x] (2025-01-10 01:00Z) Draft initial plan.
- [x] (2025-01-10 02:10Z) Implement encrypted credential fallback with stdlib encryption and tests.
- [x] (2025-01-10 02:30Z) Add profile editing with structured SSH forward UI and serialization helpers.
- [x] (2025-01-10 02:45Z) Surface server details panel and terminal/log viewer from connects and history.
- [x] (2025-01-10 03:00Z) Validate via pytest and finalize retrospective.

## Surprises & Discoveries

- Pip installation for `cryptography` is blocked by the environment proxy, so encryption was implemented with a local HMAC-based keystream instead.

## Decision Log

- Decision: Use a CustomTkinter terminal viewer bound to wlog files rather than attempting to invoke real Tera Term in this environment.
  Rationale: The app currently runs in stub mode; showing logs keeps behavior observable without external dependencies.
  Date/Author: 2025-01-10 / Assistant
- Decision: Store encrypted credentials in a local HMAC/XOR vault when keyring is unavailable.
  Rationale: Environment proxy blocks installing `cryptography`; a stdlib-only keystream still encrypts secrets at rest and satisfies the requirement.
  Date/Author: 2025-01-10 / Assistant

## Outcomes & Retrospective

- Implemented encrypted credential fallback, profile editing, flexible SSH forwarding UI, and terminal/log visibility. Tests now pass end-to-end.

## Context and Orientation

The launcher UI lives in `ForTeraterm/ui/main_window.py`, with profile creation in `ForTeraterm/ui/profile_dialog.py` and credential handling in `ForTeraterm/credential_store.py`. Connection execution is stubbed through `ForTeraterm/launcher.py`, which writes `.wlog` files. SSH options are stored on `Profile.ssh_options` and passed into the TTL renderer in `ForTeraterm/ttl_renderer.py`. Credentials are currently stored only via the OS keyring, leaving restricted environments unable to save secrets.

## Plan of Work

Expand `CredentialStore` to support an encrypted local fallback using a generated Fernet key stored on disk, enabling encrypted password persistence even without a system keyring. Update UI status text to reflect the active mode and adjust tests to cover the new path.

Enhance `ProfileDialog` to support editing existing profiles and command sets, pre-filling fields and persisting updates. Replace the free-form SSH options with a structured port-forwarding editor that can parse existing `/FWD=` entries, allow any number of forwards, and merge them with additional custom SSH options. Update storage/renderer interaction so the composed `ssh_options` string remains compatible.

In `MainWindow`, add an "Edit Profile" entry point, a server detail panel showing selected profile fields, port forwards, and commands, and a terminal viewer invoked after launches or from history selections to display the `.wlog` content. Provide a way to open the same viewer from history entries to inspect past sessions.

Cover the new behaviors with tests: credential encryption fallback round-trip, SSH option serialization/parsing, and profile editing persistence. Keep existing tests green.

## Concrete Steps

1. Implement encrypted local credential fallback in `ForTeraterm/credential_store.py`, persisting secrets with a stdlib keystream cipher and storing metadata in an app data directory; adjust status strings and tests.
2. Refactor `ForTeraterm/ui/profile_dialog.py` to support both create and edit flows, adding structured port-forwarding widgets, parsing existing options, and persisting updates to profiles and command sets.
3. Extend `ForTeraterm/ui/main_window.py` with an "Edit Profile" action, a server detail pane, and hooks to launch a terminal/log viewer after connects and from history; add the viewer component in a new module if helpful.
4. Keep TTL rendering compatible by ensuring serialized SSH options remain in the `/FWD=local=remote:port` format alongside any extra options.
5. Add unit tests in `tests/` to validate credential encryption fallback and SSH option helpers; update existing tests if needed.
6. Run `pytest -q` to verify functionality and update this plan’s progress and retrospective.

## Validation and Acceptance

- Connecting to a profile opens a terminal/log window showing the stubbed session output; viewing a history item shows the same log content.
- Editing a saved profile updates its host/user/ports/forwards and command set; subsequent connections use the edited values.
- SSH forwarding can capture multiple entries via the UI, storing them as `/FWD=` options that appear in generated TTL scripts.
- Passwords can be stored and reloaded in environments without a working keyring via encrypted local storage.
- All automated tests pass with `pytest -q`.

## Idempotence and Recovery

The encrypted credential store generates a reusable key and can be re-run safely; corrupted files should raise clear errors prompting deletion/regeneration. Profile edits are persisted via `upsert` operations; reopening dialogs pre-fills current values. The terminal viewer reads `.wlog` files without modifying them, so repeated opens are safe.

## Artifacts and Notes

- None yet.

## Interfaces and Dependencies

- `CredentialStore` gains a `mode` value of `"local_encrypted"` and uses a stdlib HMAC/XOR keystream for encryption. The store should read/write JSON in an app data directory (e.g., `~/.forteraterm/creds.json`).
- `ProfileDialog` should accept an optional existing `Profile` and `CommandSet`, expose methods to parse/build SSH options from a list of forwarding entries plus free-form extras, and reuse `upsert` to persist edits.
- `MainWindow` should expose UI affordances to edit profiles, show details, and open a terminal/log viewer window bound to `.wlog` files.
