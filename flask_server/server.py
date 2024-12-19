import os
import subprocess

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

def generate_ssl_certificates(cert_file, key_file):
    """Generate SSL certificates if they don't exist."""
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("SSL certificate or key not found. Generating new ones...")
        try:
            subprocess.run(
                [
                    "openssl", "req", "-x509", "-nodes", "-days", "365",
                    "-newkey", "rsa:2048", "-keyout", key_file, "-out", cert_file,
                    "-subj", "/C=US/ST=State/L=City/O=Organization/CN=localhost"
                ],
                check=True
            )
            print("SSL certificates successfully generated.")
        except Exception as e:
            print(f"Failed to generate SSL certificates: {e}")
            raise

def start_flask_server(queue, event):
    """Start the Flask server."""
    app = create_app(queue)

    # Check for SSL certificate and key files
    cert_file = 'cert.pem'
    key_file = 'key.pem'

    # Generate SSL certificates if not present
    try:
        generate_ssl_certificates(cert_file, key_file)
    except Exception as e:
        event.set()  # Notify parent process of failure
        return

    ssl_context = (cert_file, key_file)
    print("Starting server with SSL.")
    try:
        app.run(port=5000, ssl_context=ssl_context)
    except Exception as e:
        print(f"Error starting server: {e}")
        event.set()  # Notify parent process of failure
