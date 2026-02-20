from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from threadpilot.src.core.engine import ThreadPilotEngine

router = APIRouter()
engine = ThreadPilotEngine()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/review/{pr_id}")
def review(pr_id: str, live: bool = False) -> dict:
    result = engine.run_review(pr_id=pr_id, use_mock=not live)
    return result.payload


class BootstrapRequest(BaseModel):
    requirements_file: str = "requirements.md"


@router.post("/bootstrap")
def bootstrap(payload: BootstrapRequest) -> dict[str, int]:
    count = engine.bootstrap_from_file(payload.requirements_file)
    return {"requirements_loaded": count}
