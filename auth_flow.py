import sys
import time
import multiprocessing

from flask_server.server import start_flask_server
from utils.auth_url_generator import generate_auth_url, open_auth_url
from utils.token_exchange import exchange_auth_code_for_token
from utils.token_manager import save_token_data, load_token_data, is_token_expired, display_token_expiry

def get_tokens(config):
    """Main function to handle the OAuth flow."""
    # Load existing token data
    token_data = load_token_data()
    
    # Check if the token is valid
    if token_data and not is_token_expired(token_data):
        print("\nToken is still valid.")
        display_token_expiry(token_data)  # Display expiration details
        return token_data

    # If the token is expired or not found, start the OAuth flow
    print("\nToken is expired or not found. Starting OAuth flow.\n")

    # Create a queue to share the auth code between processes
    queue = multiprocessing.Queue()

    # Create an event to monitor SSL issues
    event = multiprocessing.Event()

    # Start Flask server in a separate process
    flask_process = multiprocessing.Process(target=start_flask_server, args=(queue, event))
    flask_process.start()

    # Wait for the Flask server to initialize
    time.sleep(1)

    if event.is_set():
        print("\nFailed to start the Flask server. Exiting.")
        flask_process.terminate()
        flask_process.join()
        sys.exit(1)  # Exit the parent process

    # Generate and open the authorization URL
    auth_url = generate_auth_url(config)
    open_auth_url(auth_url)

    # Wait for the authorization code to be received
    auth_code = None
    while auth_code is None:
        try:
            auth_code = queue.get(timeout=1)  # Wait for the auth code from the queue
        except multiprocessing.queues.Empty:
            continue

    # Exchange the authorization code for tokens
    tokens = exchange_auth_code_for_token(config, auth_code)
    if tokens:
        save_token_data(tokens)
        print("\nTokens successfully saved.")
        display_token_expiry(tokens)  # Display expiration details

        # Terminate the Flask process
        flask_process.terminate()
        flask_process.join()  # Optional: Ensure the process is fully cleaned up
        return tokens
    
    else:
        print("Failed to exchange authorization code for tokens.")
        # Terminate the Flask process
        flask_process.terminate()
        flask_process.join()  # Optional: Ensure the process is fully cleaned up
        return None

if __name__ == "__main__":
    get_tokens()
