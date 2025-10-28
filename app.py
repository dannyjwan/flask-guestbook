from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any

from flask import Flask, render_template, request, redirect, url_for, flash


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.getenv("SECRET_KEY", "dev"))

    default_data_file = Path(__file__).parent / "guestbook.json"
    data_file = Path((test_config or {}).get("DATA_FILE", os.getenv("DATA_FILE", default_data_file)))
    data_file.parent.mkdir(parents=True, exist_ok=True)

    def read_entries() -> list[dict[str, str]]:
        if not data_file.exists():
            return []
        try:
            with data_file.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def write_entry(name: str, message: str) -> None:
        entries = read_entries()
        entries.append({
            "name": name.strip()[:50] or "Anonymous",
            "message": message.strip()[:500],
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        with data_file.open("w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/")
    def index():
        entries = read_entries()[::-1]
        return render_template("index.html", entries=entries)

    @app.post("/sign")
    def sign():
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()
        if not message:
            flash("Message cannot be empty.", "error")
            return redirect(url_for("index"))
        write_entry(name or "Anonymous", message)
        flash("Thanks for signing the guestbook!", "success")
        return redirect(url_for("index"))

    return app


# WSGI entrypoint
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
