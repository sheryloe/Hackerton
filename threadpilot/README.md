# ThreadPilot MVP

ThreadPilot is a local-first MVP that tracks project state, ingests requirement context, and generates PM-oriented review packets from Git changes.

## Quick Start (Beginner)

### Option A: One-click run (recommended)
Double-click:
- `start_threadpilot_ui.bat`

What it does automatically:
- Detects `dist/threadpilot.exe` and runs it if available
- If EXE is missing: creates `.venv`, installs defaults from `requirements.txt`, launches UI

### Option B: Full default setup (install everything)
Double-click:
- `setup_default.bat`

What it does automatically:
- Creates `.venv`
- Upgrades `pip`
- Installs all dependencies
- Installs `pyinstaller`
- Builds `dist/threadpilot.exe`
- Launches UI

## Manual CLI usage

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python -m threadpilot.main ui
```

## CLI Commands

```bash
python -m threadpilot.main bootstrap --requirements-file 요구사항.md
python -m threadpilot.main review --pr 123
python -m threadpilot.main review --pr 123 --live
```

## API Endpoints

- `GET /api/health`
- `POST /api/bootstrap`
- `POST /api/review/{pr_id}?live=false`

## Data persistence

Local files are written under `threadpilot/data/`:
- `project_state.json`
- `requirements.json`
- `todo_list.md`
- `chroma/`
