import requests

def exchange_auth_code_for_token(config, auth_code):
    """Exchange the authorization code for tokens."""
    data = {
        'grant_type': 'authorization_code',
        'client_id': config['CLIENT_ID'],
        'client_secret': config['CLIENT_SECRET'],
        'code': auth_code,
        'redirect_uri': config['REDIRECT_URI'],
    }

    response = requests.post(config['TOKEN_URL'], data=data)
    if response.status_code == 200:
        tokens = response.json()
        return tokens
    else:
        print(f"Failed to get tokens: {response.status_code} - {response.text}")
        return None

def refresh_access_token(refresh_token, token_url, client_id, client_secret):
    """Exchange the refresh token for a new access token."""
    
    # Data to send in the POST request
    data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': 'gateway.stockx.com',
        'refresh_token': refresh_token
    }

    # Perform the POST request to refresh the access token
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        tokens = response.json()
        print(f"New access token: {tokens['access_token']}")
        return tokens
    else:
        print(f"Failed to refresh access token: {response.status_code} - {response.text}")
        return None