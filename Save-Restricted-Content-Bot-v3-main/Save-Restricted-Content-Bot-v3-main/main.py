import asyncio
import importlib
import os
import sys
from threading import Thread
from flask import Flask
from shared_client import start_client

# Flask app for Render port binding
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )

async def load_and_run_plugins():
    await start_client()

    plugin_dir = "plugins"
    plugins = [
        f[:-3]
        for f in os.listdir(plugin_dir)
        if f.endswith(".py") and f != "__init__.py"
    ]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")

        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()

async def main():
    await load_and_run_plugins()

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    # Start Flask server for Render
    Thread(target=run_web, daemon=True).start()

    loop = asyncio.get_event_loop()
    print("Starting clients ...")

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        try:
            loop.close()
        except Exception:
            pass    finally:
        try:
            loop.close()
        except Exception:
            pass
