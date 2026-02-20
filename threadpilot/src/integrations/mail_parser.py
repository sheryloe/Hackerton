from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ParsedMail:
    subject: str
    sender: str
    body: str


def parse_simple_mail(raw: str) -> ParsedMail:
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    subject = next((l.replace("Subject:", "").strip() for l in lines if l.startswith("Subject:")), "")
    sender = next((l.replace("From:", "").strip() for l in lines if l.startswith("From:")), "")
    body_index = next((i for i, l in enumerate(lines) if l == "---"), -1)
    body = "\n".join(lines[body_index + 1 :]) if body_index >= 0 else "\n".join(lines)
    return ParsedMail(subject=subject, sender=sender, body=body)
