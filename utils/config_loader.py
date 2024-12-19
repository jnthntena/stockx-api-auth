from dotenv import load_dotenv
import os

# Load environment variables from .env
def load_environment():
    """Load configuration from the .env file."""
    load_dotenv(override=True)
    return {
        "TOKEN_URL": os.getenv("TOKEN_URL"),
        "API_KEY": os.getenv("API_KEY"),
        "CLIENT_ID": os.getenv("CLIENT_ID"),
        "CLIENT_SECRET": os.getenv("CLIENT_SECRET"),
        "REDIRECT_URI": os.getenv("REDIRECT_URI"),
        "STATE": os.getenv("STATE"),
    }