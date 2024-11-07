from webhook.aircall_webhook import app
import requests

# Global stop flag
should_stop_flask = False

def initialize_flask_app():
    """Return the initialized Flask app."""
    return app

def run_flask():
    """Run Flask app and check periodically if it should stop."""
    global should_stop_flask
    while not should_stop_flask:
        app.run(port=5000, use_reloader=False)

def shutdown_flask():
    """Gracefully stop the Flask server by setting the stop flag."""
    global should_stop_flask
    should_stop_flask = True
    try:
        requests.post("http://localhost:5000/shutdown")  # Trigger a final request to exit
    except requests.exceptions.RequestException:
        pass  # Ignore errors during shutdown