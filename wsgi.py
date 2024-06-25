from app import app
from pathlib import Path

if __name__ == "__main__":
    app.run(f"{Path(__file__).stem}:app")
