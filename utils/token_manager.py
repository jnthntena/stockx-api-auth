from datetime import datetime, timedelta
import pytz
import time
import json
import os

TOKEN_FILE = "token_data.json"
CENTRAL_TZ = pytz.timezone("US/Central")

def save_token_data(tokens):
    """Save token data to a file."""
    data = {
        "access_token": tokens['access_token'],
        "refresh_token": tokens['refresh_token'],
        "id_token": tokens['id_token'],
        "expires_in": time.time() + tokens['expires_in']
    }
    with open(TOKEN_FILE, 'w') as f:
        json.dump(data, f)

def load_token_data():
    """Load token data from a file."""
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, 'r') as f:
        return json.load(f)

def is_token_expired(token_data):
    """Check if the token is expired."""
    return time.time() >= token_data.get("expires_in", 0)

def display_token_expiry(token_data):
    """Display token expiration details."""
    expires_in = token_data.get("expires_in", 0)
    current_time = time.time()

    # Convert expires_in (duration) to absolute timestamp if necessary
    if expires_in < 50000:  # Likely a duration, not a timestamp
        expires_in += current_time

    remaining_seconds = expires_in - current_time

    if remaining_seconds > 0:
        # Convert UNIX timestamp to Central Time
        expiry_time = datetime.fromtimestamp(expires_in, tz=pytz.utc).astimezone(CENTRAL_TZ)
        remaining_time = timedelta(seconds=remaining_seconds)

        print(f"Token expires at: {expiry_time.strftime('%Y-%m-%d %I:%M:%S %p')} Central Time")
        print(f"Time remaining until token expiration: {remaining_time}")
    else:
        print("Token has already expired.")