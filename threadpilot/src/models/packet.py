from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class DriftAnalysis(BaseModel):
    is_drift_detected: bool = False
    original_spec: str = ""
    current_impl: str = ""
    reason: str = ""


class ReviewPacket(BaseModel):
    pr_id: str
    fulfilled_requirements: List[str] = Field(default_factory=list)
    missing_requirements: List[str] = Field(default_factory=list)
    drift_analysis: DriftAnalysis = Field(default_factory=DriftAnalysis)
    impacted_modules: List[str] = Field(default_factory=list)
    new_todos_created: List[str] = Field(default_factory=list)
    suggested_actions: List[str] = Field(default_factory=list)
