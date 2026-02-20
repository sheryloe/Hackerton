from __future__ import annotations

import argparse
import json
import sys
import threading
import time
import webbrowser
from pathlib import Path

from threadpilot.src.core.engine import ThreadPilotEngine


def resolve_ui_file() -> Path:
    frozen_base = getattr(sys, "_MEIPASS", None)
    if frozen_base:
        bundled = Path(frozen_base) / "threadpilot" / "src" / "ui" / "main.html"
        if bundled.exists():
            return bundled

    local = Path(__file__).resolve().parent / "src" / "ui" / "main.html"
    if local.exists():
        return local

    adjacent = Path(sys.executable).resolve().parent / "threadpilot" / "src" / "ui" / "main.html"
    return adjacent


def build_app():
    try:
        from fastapi import FastAPI
        from fastapi.responses import FileResponse
        from threadpilot.src.api.routes import router
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("FastAPI is required to run API mode.") from exc

    app = FastAPI(title="ThreadPilot")
    app.include_router(router, prefix="/api")

    ui_file = resolve_ui_file()

    @app.get("/")
    def root() -> FileResponse:
        return FileResponse(ui_file)

    @app.get("/main.html")
    def main_html() -> FileResponse:
        return FileResponse(ui_file)

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

    ui_parser = subparsers.add_parser("ui", help="Run web UI for beginners")
    ui_parser.add_argument("--host", default="127.0.0.1", help="Host for UI server")
    ui_parser.add_argument("--port", type=int, default=8000, help="Port for UI server")
    ui_parser.add_argument("--no-open", action="store_true", help="Do not auto-open browser")

    args = parser.parse_args()
    engine = ThreadPilotEngine()

    if args.command == "review":
        result = engine.run_review(pr_id=args.pr, use_mock=not args.live)
        print(json.dumps(result.payload, ensure_ascii=False, indent=2))
    elif args.command == "bootstrap":
        total = engine.bootstrap_from_file(path=args.requirements_file)
        print(json.dumps({"requirements_loaded": total}, ensure_ascii=False, indent=2))
    elif args.command == "ui":
        try:
            import uvicorn
        except Exception as exc:
            raise RuntimeError("uvicorn is required for UI mode.") from exc

        url = f"http://{args.host}:{args.port}/"
        if not args.no_open:
            threading.Thread(target=lambda: (time.sleep(0.8), webbrowser.open(url)), daemon=True).start()
        if app is None:
            raise RuntimeError("Failed to initialize FastAPI app for UI mode.")
        uvicorn.run(app, host=args.host, port=args.port, reload=False)
    else:
        parser.print_help()


app = None
try:
    app = build_app()
except RuntimeError:
    pass


if __name__ == "__main__":
    cli()
