from __future__ import annotations

import json
from typing import Any, Optional, Type

from pydantic import BaseModel

try:
    from litellm import completion
except Exception:  # litellm not installed fallback for local MVP
    completion = None


class LLMClient:
    def __init__(self, model: str) -> None:
        self.model = model

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: Type[BaseModel],
        max_retries: int = 2,
    ) -> BaseModel:
        if completion is None:
            raise RuntimeError("litellm is not installed. Install dependencies first.")

        last_error: Optional[Exception] = None
        for _ in range(max_retries + 1):
            try:
                response: Any = completion(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format={"type": "json_object"},
                )
                content = response.choices[0].message.content
                parsed = json.loads(content)
                return response_model.model_validate(parsed)
            except Exception as exc:
                last_error = exc

        raise RuntimeError(f"Failed to parse LLM response after retries: {last_error}")
