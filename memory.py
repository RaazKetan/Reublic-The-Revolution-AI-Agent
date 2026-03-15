import json
import os
from datetime import datetime

MEMORY_FILE = "game_memory.json"

def load():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {
        "phase": "character_creation",
        "turn": 0,
        "stats": {},
        "history": [],
        "last_screenshot": None,
        "last_action": None,
        "stuck_count": 0,
    }

def save(state: dict):
    with open(MEMORY_FILE, "w") as f:
        json.dump(state, f, indent=2)

def log_action(state: dict, agent: str, action: str, reasoning: str):
    state["history"].append({
        "time": datetime.now().isoformat(),
        "agent": agent,
        "action": action,
        "reasoning": reasoning,
    })
    # keep only last 50 entries so file stays small
    state["history"] = state["history"][-50:]
    save(state)
