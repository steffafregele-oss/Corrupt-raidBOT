import os
import json

PREMIUM_FILE = "premium.json"

def load_premium():
    """Load the list of premium users."""
    if not os.path.exists(PREMIUM_FILE):
        return []
    with open(PREMIUM_FILE, "r") as f:
        return json.load(f)

def save_premium(data):
    """Save the premium list."""
    with open(PREMIUM_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_premium_user(user_id):
    """Add a user to the premium list."""
    users = load_premium()
    if user_id not in users:
        users.append(user_id)
        save_premium(users)

def remove_premium_user(user_id):
    """Remove a user from the premium list."""
    users = load_premium()
    if user_id in users:
        users.remove(user_id)
        save_premium(users)
        return True
    return False
