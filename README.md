# ForTeraterm

ForTeraterm is a desktop companion for [Tera Term](https://ttssh2.osdn.jp/index.html.en) built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). It centralises server definitions, macros, and Tera Term launch options so teams can share a consistent workflow for daily operations.

The application ships with a Windows installer (PyInstaller + Inno Setup) and can also be run directly from source on any platform supported by Python and CustomTkinter.

## Table of contents
- [Features](#features)
- [Project layout](#project-layout)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Create a virtual environment](#create-a-virtual-environment)
  - [Install dependencies](#install-dependencies)
- [Running the application](#running-the-application)
- [Managing data](#managing-data)
- [Testing](#testing)
- [Packaging for Windows](#packaging-for-windows)
- [License](#license)

## Features
- **Server registry** – capture SSH, Telnet, or serial connection details and share them via JSON files stored under `ForTeraterm/ServerData`. 【F:ForTeraterm/ServerData/serverfilemanage.py†L1-L106】
- **Macro editor** – edit and associate Tera Term macro files so that complex logins can be replayed automatically. 【F:ForTeraterm/WindowAction/editmacro.py†L1-L204】
- **Batch launcher** – start multiple servers at once, optionally running macros, from the main dashboard. 【F:ForTeraterm/WindowAction/serveraccess.py†L1-L225】
- **Theme and layout controls** – adjust window size, colours, and fonts using the built-in settings panes. 【F:ForTeraterm/WindowSettings/theme.py†L1-L118】【F:ForTeraterm/WindowSettings/edit.py†L1-L214】
- **Localisation support** – switch UI text by toggling the language configuration file. 【F:ForTeraterm/Language/apptext.py†L1-L116】

## Project layout
```
ForTeraterm/
├── ForTeraterm/            # Application package
│   ├── WindowAction/       # Frames for registry, macro editor, and launcher
│   ├── WindowSettings/     # Theme manager, configuration editors, image helpers
│   ├── Language/           # Localised UI strings
│   ├── ServerData/         # JSON persistence helpers
│   └── view_manager.py     # Utility for swapping frames inside the main window
├── img/, icons/, locales/  # Static assets bundled with the installer
├── main.py                 # CLI entry point for launching the UI
├── mkinst.iss              # Inno Setup script used when packaging for Windows
├── tests/                  # Pytest test suite covering UI helpers and managers
└── write_mkinstiss.py      # Generates the Inno Setup script from build output
```

## Getting started
### Prerequisites
- Python 3.11 or newer
- Tera Term installed locally (required once you start launching sessions)
- Windows users should install the Tera Term 64-bit binaries; macOS/Linux users can run the launcher but will need a remote Windows host for Tera Term itself.

### Clone the repository (with submodules)
The `CTkMessagebox` widget is tracked as a Git submodule. Make sure you pull it down the first time you clone:

```bash
git clone --recursive https://github.com/<your-account>/ForTeraterm.git
cd ForTeraterm

# If you already cloned without --recursive, run this once inside the repo:
git submodule update --init --recursive
```

### Create a virtual environment
```bash
python -m venv .venv
# Windows PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

### Install dependencies
Runtime dependencies are listed in `requirements.txt`. For development, including the test suite, install the `requirements-dev.txt` bundle **from the repository root**:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

## Running the application
After activating the virtual environment and installing dependencies, launch the CustomTkinter UI from the repository root with:

```bash
python main.py
```

The main window opens on the **Server Access** view. Use the **Action** menu to register servers or edit macros. All window state (size, theme, language) is saved through the configuration helpers under `ForTeraterm/WindowSettings` for the next session. 【F:ForTeraterm/main_menu.py†L1-L152】

## Managing data
Server entries and macro metadata are stored as JSON files in `ForTeraterm/ServerData`. You can back up or share these files between team members. Encryption helpers are provided so sensitive fields can be obfuscated before distribution. 【F:ForTeraterm/_config/encrypter.py†L1-L95】

## Testing
The project uses [pytest](https://docs.pytest.org/) to exercise non-graphical logic such as frame switching, file management, and dialog helpers. To run the suite:

```bash
pytest
```

Tests rely on the mock objects defined in `tests/conftest.py` to simulate CustomTkinter and Pillow in headless environments. 【F:tests/conftest.py†L1-L88】

## Packaging for Windows
The CI workflow demonstrates how to build a distributable installer:
1. Create the PyInstaller bundle using `main.spec`.
2. Run `write_mkinstiss.py` to generate the Inno Setup script for the fresh build.
3. Compile the installer with Inno Setup's `ISCC.exe`.

The generated installer places assets from `img/`, `locales/`, and `icons/` alongside the executable. Refer to `.github/workflows` in your fork or the `build.bat` script for a local build. 【F:write_mkinstiss.py†L1-L196】

## License
This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
