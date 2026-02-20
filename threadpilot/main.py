from __future__ import annotations

import argparse
import json

from threadpilot.src.core.engine import ThreadPilotEngine


def build_app():
    try:
        from fastapi import FastAPI
        from threadpilot.src.api.routes import router
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("FastAPI is required to run API mode.") from exc

    app = FastAPI(title="ThreadPilot")
    app.include_router(router, prefix="/api")
    return app


def cli() -> None:
    parser = argparse.ArgumentParser(description="ThreadPilot CLI")
    subparsers = parser.add_subparsers(dest="command")

    review_parser = subparsers.add_parser("review", help="Generate review packet")
    review_parser.add_argument("--pr", required=True, help="PR id")
    review_parser.add_argument("--live", action="store_true", help="Use live LLM instead of mock")

    bootstrap_parser = subparsers.add_parser("bootstrap", help="Ingest requirements document")
    bootstrap_parser.add_argument(
        "--requirements-file",
        default="requirements.md",
        help="Path to requirements markdown file",
    )

    args = parser.parse_args()
    engine = ThreadPilotEngine()

    if args.command == "review":
        result = engine.run_review(pr_id=args.pr, use_mock=not args.live)
        print(json.dumps(result.payload, ensure_ascii=False, indent=2))
    elif args.command == "bootstrap":
        total = engine.bootstrap_from_file(path=args.requirements_file)
        print(json.dumps({"requirements_loaded": total}, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


app = None
try:
    app = build_app()
except RuntimeError:
    pass


if __name__ == "__main__":
    cli()
