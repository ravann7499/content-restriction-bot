# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import os
import asyncio
import threading
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def welcome():
    # Render the welcome page with animated "Team SPY" text
    return render_template("welcome.html")

def run_bot():
    """Run the Telegram bot in a separate thread"""
    import sys
    import subprocess
    subprocess.run([sys.executable, "main.py"])

if __name__ == "__main__":
    # Start the bot in a background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Run the Flask web server
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
