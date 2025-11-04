import os
import json

PREMIUM_FILE = "premium.json"

def load_premium():
    if not os.path.exists(PREMIUM_FILE):
        return []
    with open(PREMIUM_FILE, "r") as f:
        return json.load(f)

def save_premium(users):
    with open(PREMIUM_FILE, "w") as f:
        json.dump(users, f, indent=2)

def add_premium_user(user_id):
    premium_users = load_premium()
    if user_id not in premium_users:
        premium_users.append(user_id)
        save_premium(premium_users)

def remove_premium_user(user_id):
    premium_users = load_premium()
    if user_id in premium_users:
        premium_users.remove(user_id)
        save_premium(premium_users)
        return True
    return False
