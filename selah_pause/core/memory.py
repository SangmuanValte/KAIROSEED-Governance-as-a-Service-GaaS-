import json
import os
from datetime import datetime

DATA_FILE = "data/journal.json"

def load_entries():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_entry(text):
    os.makedirs("data", exist_ok=True)

    entries = load_entries()

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "text": text
    }

    entries.append(entry)

    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=2)
