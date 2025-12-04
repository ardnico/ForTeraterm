# Enable real Tera Term sessions, presets, settings search, and tagging

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds. This plan must be maintained in accordance with .agent/PLANS.md.

## Purpose / Big Picture

Users should be able to launch real server sessions through Tera Term directly from the launcher, automatically run predefined command sets (including a default health-check set), continue interacting with the opened terminal, quickly search settings, and organize profiles with tags. The change should let a new user create or pick a profile, connect via Tera Term, see preset commands run, keep the session open for manual use, search settings entries, and filter profiles by tags.

## Progress

- [x] (2025-12-04 16:40Z) Drafted initial ExecPlan describing goals and approach.
- [x] (2025-12-04 17:05Z) Expanded schema and settings to support tags plus Tera Term path/stub flags with migrations and defaults.
- [x] (2025-12-04 17:18Z) Added Tera Term launch path with real invocation/tailing, seeded system health preset, and session preset selector with tagging filters in the main/profile UI.
- [x] (2025-12-04 17:25Z) Implemented searchable settings dialog with new fields and refreshed UI wiring; ran automated tests.
- [ ] (pending) Final validation/retrospective updates after any additional manual checks.

## Surprises & Discoveries

- Duplicate `_open_settings` and `_rebuild_ui` definitions existed in the main window; removed the redundant block to keep rebuild logic consistent.
- Falling back to stub mode when no Tera Term path is configured avoids breaking connects while still surfacing the missing executable in the status stream.

## Decision Log

- Decision: Seed a shared "System Health" command set and allow session-level preset selection instead of duplicating commands per profile.
  Rationale: Ensures the required basic CPU/memory/disk checks are always available and reusable without editing each profile.
  Date/Author: 2025-12-04 / agent
- Decision: When Tera Term path is absent, automatically fall back to stub streaming while emitting a warning.
  Rationale: Keeps Connect usable in environments without Tera Term while still guiding users to configure the executable for real sessions.
  Date/Author: 2025-12-04 / agent

## Outcomes & Retrospective

- Implemented tagging, preset seeding/selection, real Tera Term launch support, and searchable settings. Automated tests (`pytest -q`) pass. Manual retrospective pending further UI verification.

## Context and Orientation

Relevant code lives in `ForTeraterm/`:
- `launcher.py` handles TTL rendering and session launching; currently stubbed (`stub_mode=True`) and lacks real Tera Term invocation.
- `ttl_renderer.py` renders TTL scripts from templates in `templates/ttl/v1/basic.ttl.j2` using profile and command set data.
- `storage.py` stores `Profile`, `CommandSet`, `AppSettings`, and history in SQLite. No tag support exists; settings are limited to appearance/font only.
- `ui/main_window.py` builds the main UI with profile list, history, connect flow, and uses `Launcher` in stub mode. Profiles search by name/host only; no tag filtering.
- `ui/profile_dialog.py` creates/edits profiles and command sets. No tagging or preset selection beyond per-profile command set.
- `ui/settings_dialog.py` shows a small set of appearance/font settings with no search/filtering.
- `ui/terminal_window.py` shows live output or log files; it is non-interactive and follows CustomTkinter font handling.

The goal is to extend these areas to support tags, preset command selection (including a seeded system-info set), searchable settings, and a real Tera Term execution path that keeps the terminal usable after the preset commands run.

## Plan of Work

1. **Schema and settings expansion**: Add tag support to profiles and extend app settings to store the Tera Term executable path and a flag to allow real execution (falling back to stub mode for tests). Implement migrations to bump the schema version and persist tags (likely as a JSON/text column) plus the new settings fields. Update data classes, caching, import/export, and any search functions to include tags.
2. **Preset seeding and selection**: Introduce a built-in command set for system health (CPU/memory/disk basics) seeded at startup if missing. Allow users to pick which preset to run at connect time (defaulting to the profile’s command set), exposing available command sets in the main UI and profile dialog where appropriate.
3. **Real Tera Term launch path**: Enhance `Launcher` to execute Tera Term when `stub_mode` is False by invoking the configured executable with generated TTL and optional wlog output. Ensure the session window stays open after presets by avoiding auto-close TTL macros and by not destroying the live `TerminalWindow`. Preserve asynchronous callbacks and history recording, and make stub mode the default for tests.
4. **UI for settings search and tagging**: Add tag entry/selector to the profile dialog and display tags in the profile list/details. Provide tag-based filtering in the main window (e.g., a search field or dropdown). Enhance the settings dialog with a search box that highlights or filters available settings entries (appearance, theme, font, teraterm path, stub toggle) to satisfy the search requirement.
5. **Validation**: Update or add tests for migrations, default command set seeding, and launcher behavior (stub path). Document manual validation steps in this plan. Run the existing pytest suite and any new targeted tests.

## Concrete Steps

- Work in the repository root `/workspace/ForTeraterm`.
- Update `storage.py` schema version, migrations, data classes, and search/filter methods to include `tags` plus new settings fields; adjust import/export accordingly.
- Extend `AppSettings` to include `teraterm_path` and `use_stub` (or similar) defaults; update load/save and settings dialog to edit them.
- Seed a default command set (system info) during application startup (e.g., DataStore helper invoked by MainWindow) and expose command set choices in the connect flow.
- Modify `Launcher` to support real execution via `subprocess.Popen` when stub mode is disabled, passing TTL file and wlog path, and keep terminal windows open while recording history.
- Enhance `MainWindow` and `ProfileDialog` to manage tags and command set selection per session; show tags in lists and filters.
- Add a search field in `SettingsDialog` that filters/highlights settings entries and includes new settings fields.
- Update `terminal_window.py` if needed to support continued viewing after preset commands (e.g., status updates, reconnect behavior).
- Write or adjust tests in `tests/` for new behavior where practical; keep stub mode default for automated tests.
- Run `pytest -q` and verify UI flows manually if possible; record outcomes below.

## Validation and Acceptance

After implementation:
- Start the app (`python main.py` or equivalent) and verify that settings include Tera Term path/stub toggle and can be searched via a search box (typing “font” narrows to font controls, typing “tera” shows the executable path).
- Create or edit a profile with tags and select the system-info preset. In the main window, filter profiles by a tag and confirm the list updates. Click Connect: Tera Term should launch when a path is configured and stub mode disabled; otherwise, stub mode still shows streamed output. Preset commands appear in the terminal output and the session remains open for manual interaction.
- History entries should reflect the command set used and preserve the wlog path.
- Automated tests (`pytest -q`) pass.

## Idempotence and Recovery

Schema migrations should be safe to re-run. Seed logic must check for existing command sets to avoid duplicates. If Tera Term execution fails, fall back to stub mode with clear status messages. Cancelling a launch should stop the thread; TTL temp files should be cleaned up in `finally` blocks.

## Artifacts and Notes

- Capture any new test outputs or manual check results here after execution.

## Interfaces and Dependencies

- New settings fields: `AppSettings.teraterm_path: str` (path to executable) and `AppSettings.use_stub: bool` (default True for tests). Stored in `preferences` table as strings.
- New profile field: `tags: list[str]` stored in DB as JSON/text; searchable and displayed in UI.
- Launcher real mode: call `subprocess.Popen([teraterm_path, f"/R={ttl_file}", f"/W={wlog_path}"])` or similar; wait for completion up to timeout; stream wlog tail into UI when possible.

