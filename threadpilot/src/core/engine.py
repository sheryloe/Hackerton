from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from threadpilot.config import DEFAULT_MODEL, REQUIREMENTS_FILE, STATE_FILE, TODO_FILE
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
        return "unknown"

    def run_review(self, pr_id: str, use_mock: bool = True) -> EngineResult:
        state = self.state_manager.load(project_id="threadpilot")
        commits = self.git_client.recent_commits(limit=5)
        diff_text = self.git_client.pr_diff()
        _ = self.git_client.summarize_for_llm(commits, diff_text)

        if use_mock:
            packet = self.reviewer.generate_mock(pr_id=pr_id, requirements=state.requirements)
        else:
            packet = self.reviewer.generate(pr_id=pr_id, diff_text=diff_text, requirements=state.requirements)

        updated_state = self.syncer.sync(state, packet)
        self.state_manager.save(updated_state)
        return EngineResult(intent="review", payload=packet.model_dump())
