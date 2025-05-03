from flask import Flask
import threading
import logging
import os

# Main Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from your main app!"

# Keep-alive function using a separate Flask server
def start_keep_alive():
    try:
        keep_alive_app = Flask('keep_alive')

        @keep_alive_app.route('/')
        def keep_home():
            return "Keep-alive server is running."

        def run():
            keep_alive_app.run(host='0.0.0.0', port=8080)

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        return True
    except Exception as e:
        print(f"Failed to start keep-alive: {e}")
        return False

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Main execution
if __name__ == "__main__":
    # Start keep-alive server
    keep_alive_started = start_keep_alive()

    if keep_alive_started:
        logger.info("Keep-alive service running on port 8080")
    else:
        logger.warning("Failed to start keep-alive service")

    # Run main app
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
