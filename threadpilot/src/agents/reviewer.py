from __future__ import annotations

from typing import List

from threadpilot.src.core.llm_client import LLMClient
from threadpilot.src.models.packet import DriftAnalysis, ReviewPacket
from threadpilot.src.models.schema import FeatureReq


SYSTEM_PROMPT = (
    "You are a project review analyst for PM/operations stakeholders. "
    "Analyze requirement fulfillment, scope drift, and operational impact. "
    "Return only valid ReviewPacket JSON."
)


class ReviewPacketGenerator:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    def generate(self, pr_id: str, diff_text: str, requirements: List[FeatureReq]) -> ReviewPacket:
        req_text = "\n".join(
            [f"- {req.id}: {req.description} ({req.status})" for req in requirements]
        ) or "- none"

        user_prompt = (
            f"PR ID: {pr_id}\n"
            f"Requirements:\n{req_text}\n\n"
            "Analyze this diff and return a ReviewPacket JSON.\n"
            f"Diff:\n{diff_text[:8000]}"
        )
        return self.llm_client.complete_json(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=ReviewPacket,
        )

    def generate_mock(self, pr_id: str, requirements: List[FeatureReq]) -> ReviewPacket:
        req_ids = [r.id for r in requirements]
        fulfilled = req_ids[:1]
        missing = req_ids[1:]
        new_todos = ["Validate missing requirements with product owner"]
        if missing:
            new_todos.append("Update spec and acceptance tests for uncovered requirements")

        return ReviewPacket(
            pr_id=pr_id,
            fulfilled_requirements=fulfilled,
            missing_requirements=missing,
            drift_analysis=DriftAnalysis(
                is_drift_detected=bool(missing),
                original_spec="Requirements loaded from project state",
                current_impl="Current diff addresses only a subset of requirements",
                reason="Unfulfilled requirements remain after diff inspection",
            ),
            impacted_modules=["agents/reviewer.py", "core/state_manager.py"],
            new_todos_created=new_todos,
            suggested_actions=[
                "Align implementation plan with requirement coverage matrix",
                "Create or update QA scenarios for changed modules",
            ],
        )
