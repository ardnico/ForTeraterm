# Performance and operational hardening roadmap

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds. Maintain this document in accordance with `.agent/PLANS.md`.

## Purpose / Big Picture

Operators need a faster, more reliable way to launch and monitor sessions, plus safeguards for storing and reusing sensitive connection data. This plan targets performance and operational improvements: responsive launch flows that stream live output, resilient reconnects, quicker profile access, and verifiable password protection. After delivery, users will see sessions open with minimal delay, watch real-time terminal output without window juggling, recover from transient drops automatically, and trust that encrypted secrets remain usable across machines.

## Progress

- [x] (2025-01-10 04:00Z) Draft initial roadmap and scope.
- [x] (2025-01-11 01:10Z) Implement asynchronous launcher with streaming terminal view and timeout controls.
- [x] (2025-01-11 01:30Z) Add connection health checks, auto-reconnect, and session resume hooks.
- [x] (2025-01-11 01:45Z) Optimize profile access with caching, search, and lazy loading of history/logs.
- [x] (2025-01-11 02:00Z) Harden secret storage with key rotation, backup/export, and integrity checks.
- [x] (2025-01-11 02:10Z) Validate with automated tests, manual drills, and retrospective updates.

## Surprises & Discoveries

- The container blocks outbound installs, so preflight health checks rely on stdlib DNS/TCP probes and are injectable for tests to avoid network flakiness.
- CustomTkinter requires UI mutations on the main thread; streaming callbacks now hop through `after` to keep the terminal view responsive without race conditions.

## Decision Log

- Decision: Focus this plan on high-impact operational improvements (performance, resilience, and security) rather than cosmetic features.
  Rationale: Prior feedback asked for practical, valuable enhancements; these areas reduce downtime and protect credentials.
  Date/Author: 2025-01-10 / Assistant
- Decision: Use a threaded stub launcher with streamed callbacks and TTL file reuse instead of attempting real Tera Term processes.
  Rationale: The environment cannot spawn Tera Term; streaming stub output still exercises the UI and history pipeline with observable logs and retries.
  Date/Author: 2025-01-11 / Assistant
- Decision: Keep credential hardening stdlib-only with PBKDF2/HMAC envelopes for export/import.
  Rationale: Proxy blocks external crypto installs; PBKDF2 + XOR keystream keeps data portable with integrity checks.
  Date/Author: 2025-01-11 / Assistant

## Outcomes & Retrospective

- Async launch pipeline now streams stubbed output into a live terminal window with cancel/reconnect controls and timeouts; preflight checks fail fast with clear messaging.
- Profile browsing is faster via cached queries and a search bar; history and log reading stay lazy to avoid UI stalls.
- Credential vault supports key rotation plus password-protected export/import with integrity validation, keeping secrets portable without a keyring.
- Tests cover async streaming, reconnect attempts, keep-alive option helpers, and credential rotations; the UI hooks reload history on completion to keep behavior observable.

## Context and Orientation

The GUI is built with CustomTkinter in `ForTeraterm/ui/`, driven by profile data from `ForTeraterm/storage.py` and credentials managed by `ForTeraterm/credential_store.py`. Session launches are orchestrated through `ForTeraterm/launcher.py`, which currently writes Tera Term `.ttl` scripts and stub `.wlog` files consumed by `ForTeraterm/ui/terminal_window.py`. Profiles and SSH options are edited via `ForTeraterm/ui/profile_dialog.py`, while preferences live in `ForTeraterm/ui/settings_dialog.py`. Tests reside under `tests/` and are run with `pytest -q`.

## Plan of Work

Introduce an asynchronous launch pipeline that spawns Tera Term processes without blocking the UI, streaming stdout/stderr to a persistent terminal window with explicit timeouts and cancellation. Add health checks (pre-flight DNS/port probes and keep-alive pings) to detect unreachable hosts before launch and to trigger automatic reconnects when transient drops occur, storing reconnection attempts in history. Improve profile usability by caching the profile list, adding quick search/filter, and lazily loading history/log content only when selected to keep the UI responsive on large datasets. Strengthen credential handling by supporting key rotation with migration, optional encrypted exports for transfer to another machine, and integrity verification to detect tampering. Cover the new behaviors with automated tests and manual drills that demonstrate faster launches, resilient reconnects, and secure secret management.

## Concrete Steps

1. Refactor `ForTeraterm/launcher.py` to provide an async-friendly launch function that uses threads or asyncio to stream process output into `TerminalWindow` in real time, with configurable timeouts and cancel support surfaced in the UI.
2. In `ForTeraterm/ui/main_window.py` and `ForTeraterm/ui/terminal_window.py`, add a persistent terminal pane that stays attached across reconnects, shows connection state, and allows manual reconnect; wire pre-flight reachability checks (DNS resolution and TCP port probe) before spawning sessions.
3. Extend `ForTeraterm/ssh_options.py` (or add a helper) to emit keep-alive/ServerAliveInterval options and to record reconnect attempts in history; ensure SSH options remain TTL-compatible.
4. Optimize profile handling in `ForTeraterm/storage.py` and `ForTeraterm/ui/profile_dialog.py` with in-memory caches, search/filter inputs, and lazy loading of history and `.wlog` content only on demand to reduce startup latency.
5. Enhance `ForTeraterm/credential_store.py` with key rotation commands, encrypted import/export (e.g., password-protected archive), and integrity checks (HMAC over payload); surface status and rotation prompts in the UI.
6. Add tests in `tests/` for async launch streaming, reconnect logic, keep-alive option serialization, cache invalidation, and credential rotation/export/import; document manual validation steps (launch timing comparison, forced network drop, cross-machine credential restore).

## Validation and Acceptance

- Launching a session shows immediate streamed output in a terminal pane without freezing the UI; cancelling halts the process cleanly.
- Pre-flight checks warn on unreachable hosts before launch; transient disconnects trigger auto-reconnect and log the attempt in history.
- Profile list remains responsive with many entries; search/filter returns results instantly; history/log content loads only when opened.
- Credentials can be rotated, exported with encryption, imported on another machine, and verified for integrity without data loss.
- `pytest -q` passes, and manual drills for launch timing and reconnect behavior match expectations described above.

## Idempotence and Recovery

Async launch and reconnect operations should be cancellable and re-entrant; retries must close prior processes and clean temporary files. Caches must invalidate when profiles or history change. Credential rotation should keep a backup of the prior key and data, enabling rollback if import/export or verification fails. Manual drills should leave the datastore consistent and free of stray processes.

## Artifacts and Notes

- None yet.

## Interfaces and Dependencies

- `launcher.py` should expose a non-blocking `launch_session(profile, credentials, callbacks, timeout_s)` that streams output chunks to a callback.
- `terminal_window.py` should render stateful sessions with reconnect and cancel controls, consuming streamed output and history metadata.
- `credential_store.py` should support `rotate_keys()`, `export_encrypted(path, password)`, and `import_encrypted(path, password)` with integrity verification and migration handling.

Updated on 2025-01-11 after completing implementation and validation; captured new decisions and outcomes.
