from __future__ import annotations

from typing import List

from threadpilot.src.models.schema import FeatureReq


def extract_requirements_from_text(text: str) -> List[FeatureReq]:
    reqs: List[FeatureReq] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        clean = line.strip()
        if not clean:
            continue
        if clean.startswith(("-", "*")):
            reqs.append(FeatureReq(id=f"REQ-{idx}", description=clean[1:].strip()))
    return reqs
