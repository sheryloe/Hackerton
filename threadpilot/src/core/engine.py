from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from threadpilot.config import DEFAULT_MODEL, REQUIREMENTS_FILE, STATE_FILE, TODO_FILE
from threadpilot.src.agents.requirements import extract_requirements_from_text
from threadpilot.src.agents.reviewer import ReviewPacketGenerator
from threadpilot.src.agents.syncer import StateSyncer
from threadpilot.src.core.llm_client import LLMClient
from threadpilot.src.core.state_manager import StateManager
from threadpilot.src.integrations.git_client import GitClient


@dataclass
class EngineResult:
    intent: str
    payload: Dict[str, Any]


class ThreadPilotEngine:
    def __init__(self) -> None:
        self.state_manager = StateManager(STATE_FILE)
        self.git_client = GitClient(".")
        self.reviewer = ReviewPacketGenerator(LLMClient(DEFAULT_MODEL))
        self.syncer = StateSyncer(REQUIREMENTS_FILE, TODO_FILE)

    def classify_intent(self, command: str) -> str:
        lower = command.lower()
        if "review" in lower or "pr" in lower:
            return "review"
        if "sync" in lower:
            return "sync"
        if "ingest" in lower or "bootstrap" in lower:
            return "bootstrap"
        return "unknown"

    def ingest_requirements(self, text: str, project_id: str = "threadpilot") -> int:
        state = self.state_manager.load(project_id=project_id)
        extracted = extract_requirements_from_text(text)

        existing = {req.id: req for req in state.requirements}
        existing_desc = {req.description for req in state.requirements}
        for req in extracted:
            if req.id in existing:
                existing[req.id].description = req.description
            elif req.description not in existing_desc:
                state.requirements.append(req)
                existing_desc.add(req.description)

        self.state_manager.save(state)
        return len(state.requirements)

    def bootstrap_from_file(self, path: str | Path, project_id: str = "threadpilot") -> int:
        req_file = Path(path)
        if not req_file.exists() or req_file.is_dir():
            return 0
        text = req_file.read_text(encoding="utf-8", errors="ignore")
        return self.ingest_requirements(text=text, project_id=project_id)

    def _bootstrap_if_needed(self, project_id: str = "threadpilot") -> None:
        state = self.state_manager.load(project_id=project_id)
        if state.requirements:
            return

        candidates = [Path("requirements.md"), Path("README.md")]
        candidates.extend(sorted(Path(".").glob("*.md")))

        best_count = 0
        best_path: Path | None = None
        for candidate in candidates:
            if not candidate.exists() or candidate.is_dir():
                continue
            content = candidate.read_text(encoding="utf-8", errors="ignore")
            count = len(extract_requirements_from_text(content))
            if count > best_count:
                best_count = count
                best_path = candidate

        if best_path is not None:
            self.bootstrap_from_file(best_path, project_id=project_id)

    def run_review(self, pr_id: str, use_mock: bool = True) -> EngineResult:
        self._bootstrap_if_needed(project_id="threadpilot")
        state = self.state_manager.load(project_id="threadpilot")

        commits = self.git_client.recent_commits(limit=5)
        diff_text = self.git_client.pr_diff()
        _ = self.git_client.summarize_for_llm(commits, diff_text)

        if use_mock:
            packet = self.reviewer.generate_mock(pr_id=pr_id, requirements=state.requirements)
        else:
            packet = self.reviewer.generate(
                pr_id=pr_id,
                diff_text=diff_text,
                requirements=state.requirements,
            )

        updated_state = self.syncer.sync(state, packet)
        self.state_manager.save(updated_state)
        return EngineResult(intent="review", payload=packet.model_dump())
