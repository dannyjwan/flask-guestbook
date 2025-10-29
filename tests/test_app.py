import importlib
import json
import os
import sys
from pathlib import Path

import pytest

# Ensure repo root is importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_index_and_sign(tmp_path: Path, monkeypatch):
    # Route app data to a temp file for isolation
    data_file = tmp_path / "guestbook.json"
    monkeypatch.setenv("DATA_FILE", str(data_file))

    app_module = importlib.import_module("app")
    importlib.reload(app_module)
    app = app_module.create_app()
    app.testing = True
    client = app.test_client()

    # Index loads
    r = client.get("/")
    assert r.status_code == 200

    # Empty message should fail with flash and redirect
    r = client.post("/sign", data={"name": "", "message": ""}, follow_redirects=False)
    assert r.status_code == 302

    # Valid post
    r = client.post("/sign", data={"name": "Alice", "message": "Hello"}, follow_redirects=True)
    assert r.status_code == 200

    # Data file created and contains entry
    assert data_file.exists()
    data = json.loads(data_file.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["name"] == "Alice"
    assert data[0]["message"] == "Hello"
