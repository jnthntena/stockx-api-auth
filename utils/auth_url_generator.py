import webbrowser

def generate_auth_url(config):
    """Generate the authorization URL."""
    return (
        f"https://accounts.stockx.com/authorize?"
        f"response_type=code&client_id={config['CLIENT_ID']}&"
        f"redirect_uri={config['REDIRECT_URI']}&"
        f"scope=offline_access%20openid&audience=gateway.stockx.com&state={config['STATE']}"
    )

def open_auth_url(auth_url):
    """Open the authorization URL in the default web browser."""
    print(f"Opening authorization URL: {auth_url}")
    webbrowser.open(auth_url)