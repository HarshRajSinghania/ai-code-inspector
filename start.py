# start.py (Root folder mein)
import sys
import os
import uvicorn

# Project root aur app folder dono ko path mein inject karo
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "app"))

from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
