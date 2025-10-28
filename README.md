# Flask Guestbook

A minimal guestbook web app built with Flask. Stores entries in a local JSON file.

## Run locally
1) Create a venv and install deps
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
2) Start the app
```powershell
python app.py
```
Open http://127.0.0.1:5000

## Tests
```powershell
pip install -r requirements-dev.txt
pytest
```

## Project structure
- `app.py` – Flask app (factory + routes)
- `templates/index.html` – UI
- `static/styles.css` – styles
- `guestbook.json` – created at first post (ignored by git)

## Deploy
- Render: create a Web Service, build command `pip install -r requirements.txt`, start command `python app.py`.
- Railway/Heroku‑like: set start command similarly or use `flask --app app run --host 0.0.0.0`.
