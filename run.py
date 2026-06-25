"""
Entry point: python run.py
Opens the app in your browser automatically.
"""
import os
import sys
import time
import threading
import webbrowser
import uvicorn

PORT = int(os.environ.get("PORT", 8000))


def open_browser():
    time.sleep(1.5)
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    if "--no-browser" not in sys.argv:
        threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,
    )
