"""
Entry point.
- Local:   python run.py          → opens browser automatically
- Hosted:  python run.py --no-browser  → skips browser open (Railway, Render, etc.)
"""
import os
import sys
import time
import threading
import webbrowser
import uvicorn

PORT = int(os.environ.get("PORT", 8000))
NO_BROWSER = "--no-browser" in sys.argv


def open_browser():
    time.sleep(1.5)
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    if not NO_BROWSER:
        threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,
    )
