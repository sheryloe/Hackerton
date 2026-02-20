from __future__ import annotations

import re
from typing import List

from threadpilot.src.models.schema import FeatureReq


def extract_requirements_from_text(text: str) -> List[FeatureReq]:
    reqs: List[FeatureReq] = []
    seen: set[str] = set()

    bullet_pattern = re.compile(r"^([-*]|\d+[.)])\s+")
    for idx, line in enumerate(text.splitlines(), start=1):
        clean = line.strip()
        if not clean or len(clean) < 3:
            continue

        if bullet_pattern.match(clean):
            description = bullet_pattern.sub("", clean).strip()
        elif clean.endswith(":") or clean.endswith("?"):
            description = clean.rstrip(":?").strip()
        else:
            continue

        if description and description not in seen:
            seen.add(description)
            reqs.append(FeatureReq(id=f"REQ-{idx}", description=description))
    return reqs
