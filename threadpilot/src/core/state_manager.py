from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from threadpilot.src.models.schema import ProjectState


class StateManager:
    def __init__(self, state_file: Path) -> None:
        self.state_file = state_file
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self, project_id: str = "default") -> ProjectState:
        if not self.state_file.exists():
            state = ProjectState(project_id=project_id)
            self.save(state)
            return state

        try:
            payload = json.loads(self.state_file.read_text(encoding="utf-8"))
            return ProjectState.model_validate(payload)
        except Exception:
            state = ProjectState(project_id=project_id)
            self.save(state)
            return state

    def save(self, state: ProjectState) -> None:
        state.last_updated = datetime.utcnow()
        self.state_file.write_text(
            state.model_dump_json(indent=2), encoding="utf-8"
        )
