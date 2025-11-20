# TeraTerm Connection Launcher v3

A CustomTkinter-based launcher that renders TTL macros, hands secrets to Tera Term (or a built-in stub), and records history so you can reconnect with minimal clicks. Credentials are stored through the OS keyring when available and fall back to a manual input mode in locked-down environments.

## Key capabilities
- **Profiles + command sets:** Store host/user/port/auth info alongside reusable command lists rendered into TTL templates.
- **Credential lifecycle:** Save secrets via `keyring` + Windows Credential Manager when available; otherwise stay in restricted mode and prompt each launch.
- **TTL lint + stub executor:** Validate context, render `templates/ttl/v1/basic.ttl.j2`, and execute through a Python stub that simulates `/WLOG` parsing in CI-friendly environments.
- **History:** Persist result/error codes and WLOG paths per profile for quick re-run diagnostics.

## Getting started
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
   python -m pip install --upgrade pip
   python -m pip install -r requirements-dev.txt
   ```
2. Run the launcher:
   ```bash
   python main.py
   ```
3. Use **New Profile** to register a target. If credential storage is enabled you can save a credential; otherwise you will be prompted at connect time.

## Data storage
- SQLite DB at `~/.for_teraterm/launcher.db` keeps profiles, command sets, and connection history.
- Secrets are **never** stored in the DB. When available, they are written to the OS keyring under the `tt-launcher` namespace.
- JSON export/import uses schema_version `1` (see `DataStore.export_data`).

## Testing
Run the unit tests (TTL renderer, credential detection, and datastore flows):
```bash
pytest
```

## Notes on Tera Term integration
The current environment defaults to **stub mode**; TTL files are rendered and a simulated WLOG is produced for diagnosis. Swap out stub mode in `Launcher` when running on Windows with Tera Term installed.

### Credential storage note
The repository vendors a minimal `keyring` stub so tests run without external dependencies. On Windows, install the real [`keyring`](https://pypi.org/project/keyring/) package to use Credential Manager; the app will automatically detect the backend and toggle between standard and restricted modes.
