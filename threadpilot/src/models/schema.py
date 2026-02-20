from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class ProjectStatus(str, Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    RELEASE_READY = "release_ready"


class FeatureReq(BaseModel):
    id: str
    description: str
    status: str = Field(default="pending", description="pending, implemented, verified")
    linked_files: List[str] = Field(default_factory=list)


class ProjectState(BaseModel):
    project_id: str
    current_phase: ProjectStatus = ProjectStatus.PLANNING
    requirements: List[FeatureReq] = Field(default_factory=list)
    active_todos: List[str] = Field(default_factory=list)
    risk_level: str = Field(default="low", description="low, medium, high")
    last_updated: datetime = Field(default_factory=datetime.utcnow)
