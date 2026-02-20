from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STATE_FILE = DATA_DIR / "project_state.json"
REQUIREMENTS_FILE = DATA_DIR / "requirements.json"
TODO_FILE = DATA_DIR / "todo_list.md"
CHROMA_DIR = DATA_DIR / "chroma"

DEFAULT_MODEL = "gpt-4o-mini"
