# Add theme and font customization

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds. Maintain this document in accordance with `.agent/PLANS.md`.

## Purpose / Big Picture

Users want control over the launcher’s look and feel. After this change, they can choose a color theme (light/dark/system with CustomTkinter color palettes) and a preferred font family/size. Preferences must persist across restarts so the UI opens with the last selected style.

## Progress

- [x] (2025-01-10 00:00Z) Draft initial plan.
- [x] (2025-01-10 00:20Z) Implement settings persistence with schema update.
- [x] (2025-01-10 00:40Z) Add UI to view/update theme and font preferences.
- [x] (2025-01-10 00:55Z) Apply preferences to the main window widgets and validate behavior.

## Surprises & Discoveries

- None yet.

## Decision Log

- Decision: Store preferences in SQLite rather than a separate config file to keep settings alongside existing profile data and reuse the datastore lifecycle.
  Rationale: Reduces new dependencies and keeps persistence centralized.
  Date/Author: 2025-01-10 / Assistant

## Outcomes & Retrospective

- Preferences persist via SQLite and drive the launcher’s appearance and fonts on startup. UI toggles apply immediately without breaking profile selection or history filters.

## Context and Orientation

The launcher UI lives in `ForTeraterm/ui/main_window.py` and starts from `main.py`. Persistent data is handled via `ForTeraterm/storage.py`, which owns SQLite schema creation/migration. There is currently no settings persistence. CustomTkinter controls are used throughout the UI, with some raw Tk widgets for list boxes and text areas.

## Plan of Work

Expand the SQLite schema to include a `preferences` table and expose helper methods on `DataStore` to load and save an `AppSettings` dataclass (appearance mode, color theme, font family, font size). Migrate existing databases to the new schema version.

Create a new `SettingsDialog` in `ForTeraterm/ui/settings_dialog.py` that surfaces dropdowns for appearance mode and color theme, plus inputs for font family and size (with sane defaults and validation). Add a “Settings” entry point in the main window (button near the status bar) to open the dialog. When the dialog is confirmed, persist the settings via the datastore and immediately apply them to the UI.

Introduce helper methods on `MainWindow` to build and update shared `CTkFont`/Tk font instances and reconfigure existing widgets. Apply appearance/color themes via `customtkinter.set_appearance_mode` and `set_default_color_theme` before constructing widgets so initial render respects stored settings.

## Concrete Steps

1. Update `ForTeraterm/storage.py` to bump schema version, create/migrate a `preferences` table, and add `AppSettings` plus load/save helpers.
2. Add `ForTeraterm/ui/settings_dialog.py` implementing the dialog UI and returning updated settings.
3. Modify `ForTeraterm/ui/main_window.py` to load settings at startup, apply appearance/color themes, construct shared fonts, add a Settings button, and wire dialog results to persistence and live UI updates.
4. Add tests in `tests/` validating settings persistence and application (e.g., storing/loading defaults, applying updates triggers theme/font change calls where feasible).

## Validation and Acceptance

- Launching the app after saving preferences should open with the chosen appearance mode/color theme and the selected font reflected in labels/buttons/list boxes.
- Database migration from a pre-existing file succeeds, and loading settings returns defaults when no preferences are saved.
- Automated tests pass (`pytest -q`).

## Idempotence and Recovery

Schema migrations are additive and versioned; rerunning the app safely ensures the `preferences` table exists. The settings dialog writes preferences atomically through the datastore; reopening the dialog shows the last saved values. If invalid font size is entered, validation prevents saving and keeps previous values intact.

## Artifacts and Notes

- None yet.

## Interfaces and Dependencies

- `ForTeraterm/storage.py` will expose an `AppSettings` dataclass with fields `appearance_mode: str`, `color_theme: str`, `font_family: str`, `font_size: int`, plus `load_settings()` and `save_settings(settings: AppSettings)` methods.
- `ForTeraterm/ui/settings_dialog.py` will expose `SettingsDialog(ctk.CTkToplevel)` with properties to return the chosen `AppSettings`.
