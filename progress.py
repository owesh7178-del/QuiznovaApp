# progress.py
import json
import os

DEFAULT_PROGRESS = {
    "username": "Player1",
    "total_coins": 100,
    "total_score": 0,
    "xp": 0,
    "highest_level": 1,
    "unlocked_levels": [1],
    "completed_levels": {},  # "1": stars_earned
    "achievements": [],
    "settings": {"dark_mode": True, "sound": True, "music": True}
}

FILE_PATH = "progress.json"

def load_progress():
    if not os.path.exists(FILE_PATH):
        save_progress(DEFAULT_PROGRESS)
        return DEFAULT_PROGRESS
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return DEFAULT_PROGRESS

def save_progress(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)