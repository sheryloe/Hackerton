from __future__ import annotations

from fastapi import APIRouter

from threadpilot.src.core.engine import ThreadPilotEngine

router = APIRouter()
engine = ThreadPilotEngine()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/review/{pr_id}")
def review(pr_id: str) -> dict:
    result = engine.run_review(pr_id=pr_id, use_mock=True)
    return result.payload
