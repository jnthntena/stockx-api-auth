import os

from flask import Flask, request

def create_app(queue):
    """Create and configure the Flask app."""
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Welcome to the StockX OAuth handler."

    @app.route("/callback")
    def callback():
        """Handle the OAuth callback."""
        auth_code = request.args.get("code")
        if auth_code:
            queue.put(auth_code)  # Send the auth code to the queue
            shutdown_server()
            return f"Authorization code received: {auth_code}", 200
        else:
            return "No authorization code received.", 400

    def shutdown_server():
        """Shut down the Flask server."""
        try:
            func = request.environ.get("werkzeug.server.shutdown")
            if func:
                func()
            else:
                print("Server is not running with Werkzeug.")
        except Exception as e:
            print(f"Error during shutdown: {e}")

    return app

def start_flask_server(queue, event):
    """Start the Flask server."""
    app = create_app(queue)

    # Check for SSL certificate and key files
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    use_ssl = os.path.exists(cert_file) and os.path.exists(key_file)

    if use_ssl:
        print("SSL certificate and key found. Starting server with SSL.")
        ssl_context = (cert_file, key_file)
    else:
        print(
            "SSL certificate or key not found.\n"
            "\nPlease create 'cert.pem' and 'key.pem' files manually using the following command:\n"
            "\n  openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem\n"
            "\nExiting server startup."
        )
        event.set()  # Notify parent process of failure
        return

    try:
        app.run(port=5000, ssl_context=ssl_context)
    except Exception as e:
        print(f"Error starting server: {e}")
        event.set()  # Notify parent process of failure
