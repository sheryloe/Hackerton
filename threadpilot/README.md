# ThreadPilot MVP

## Quick start

```bash
pip install fastapi uvicorn pydantic gitpython litellm chromadb
python -m threadpilot.main review --pr 123
```

Run API:

```bash
uvicorn threadpilot.main:app --reload
```
