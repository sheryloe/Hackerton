from __future__ import annotations

from typing import List

from threadpilot.src.core.llm_client import LLMClient
from threadpilot.src.models.packet import ReviewPacket
from threadpilot.src.models.schema import FeatureReq


SYSTEM_PROMPT = (
    "당신은 시니어 PM/운영자 관점 리뷰어입니다. "
    "개발자 관점이 아니라 운영 리스크, 요구사항 충족도, 스펙 드리프트를 분석하세요. "
    "반드시 JSON 객체만 반환하세요."
)


class ReviewPacketGenerator:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    def generate(self, pr_id: str, diff_text: str, requirements: List[FeatureReq]) -> ReviewPacket:
        req_text = "\n".join([f"- {req.id}: {req.description} ({req.status})" for req in requirements])
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
        return ReviewPacket(
            pr_id=pr_id,
            fulfilled_requirements=req_ids[:1],
            missing_requirements=req_ids[1:],
            impacted_modules=["agents/reviewer.py", "core/state_manager.py"],
            new_todos_created=["미구현 요구사항 보완", "API 문서 업데이트 초안 작성"],
            suggested_actions=["요구사항 누락분 재개발", "QA 시나리오 보강"],
        )
