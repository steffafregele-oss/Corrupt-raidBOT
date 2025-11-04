from flask import Flask
from threading import Thread

# Creează serverul Flask
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"  # răspuns simplu pentru uptime check

def run():
    # Pornește serverul pe toate interfețele, port 8080 (Render necesită port fix)
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    # Rulează serverul Flask într-un thread separat, astfel încât botul să continue să funcționeze
    t = Thread(target=run)
    t.start()
