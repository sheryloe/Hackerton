# ThreadPilot MVP

ThreadPilot is a local-first MVP that tracks project state, ingests requirement context, and generates a PM-oriented review packet from Git changes.

## 1) Environment setup

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## 2) Bootstrap project requirements

If your document is `requirements.md`:

```bash
python -m threadpilot.main bootstrap --requirements-file requirements.md
```

If your document has a different filename (for example Korean names), pass that file path explicitly.

## 3) Run CLI review

Mock mode (no API key needed):

```bash
python -m threadpilot.main review --pr 123
```

Live LLM mode:

```bash
set OPENAI_API_KEY=your_key_here
python -m threadpilot.main review --pr 123 --live
```

## 4) Run API server

```bash
uvicorn threadpilot.main:app --reload
```

Endpoints:
- `GET /api/health`
- `POST /api/bootstrap`
- `POST /api/review/{pr_id}?live=false`

## Data persistence

Local state files are written under `threadpilot/data/`:
- `project_state.json`
- `requirements.json`
- `todo_list.md`
- `chroma/`
