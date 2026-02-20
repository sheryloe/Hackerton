from __future__ import annotations

import json
from pathlib import Path

from threadpilot.src.models.packet import ReviewPacket
from threadpilot.src.models.schema import ProjectState


class StateSyncer:
    def __init__(self, requirements_file: Path, todo_file: Path) -> None:
        self.requirements_file = requirements_file
        self.todo_file = todo_file
        self.requirements_file.parent.mkdir(parents=True, exist_ok=True)
        self.todo_file.parent.mkdir(parents=True, exist_ok=True)

    def sync(self, state: ProjectState, packet: ReviewPacket) -> ProjectState:
        fulfilled = set(packet.fulfilled_requirements)
        for req in state.requirements:
            if req.id in fulfilled:
                req.status = "implemented"

        existing_todos = set(state.active_todos)
        existing_todos.update(packet.new_todos_created)
        state.active_todos = sorted(existing_todos)

        self.requirements_file.write_text(
            json.dumps([r.model_dump() for r in state.requirements], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        self.todo_file.write_text(
            "\n".join(f"- [ ] {todo}" for todo in state.active_todos) + "\n",
            encoding="utf-8",
        )
        return state
