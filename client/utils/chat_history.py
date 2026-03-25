import json
import os

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "chat_history.json")

def load_history():
    """Load chat history from disk. Returns empty list if no history exists."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(messages):
    """Save current chat history to disk."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def clear_history():
    """Delete saved chat history file."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
