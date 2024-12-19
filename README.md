# StockX API Token Retriever

This repository provides a simple utility for retrieving API tokens using the official [StockX API](https://developer.stockx.com/). It is designed for developers who need to quickly authenticate and interact with the StockX API.

---

## Features
- Automated OAuth flow for the StockX API.
- Secure storage of tokens for future use.
- Easy integration with your projects to make authenticated API requests.

## Getting Started

### Prerequisites
Ensure you have the following installed on your system:
- **Python 3.7+**
- **pip** (Python package manager)

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/jnthntena/stockx-api-auth.git
   cd stockx-api-auth
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Generate the required SSL certificate and key files:
   ```bash
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem
   ```
   - You will be prompted to enter information for the certificate (e.g., country, organization). You can leave most fields blank if not needed.
   - This will generate `key.pem` and `cert.pem`, which are required for the Flask server to handle secure communication.

---

## Configuration
Create a `.env` file in the root directory based on the provided template:

```env
TOKEN_URL = "https://accounts.stockx.com/oauth/token"
API_KEY = "your_api_key"
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "https://127.0.0.1:5000/callback"
STATE = "random_state_string"
```

### How to Get Your API Keys and Credentials
1. Visit the [StockX Developer Portal](https://developer.stockx.com/portal/getting-started/).
2. Follow the guide for [authentication](https://developer.stockx.com/portal/authentication/).
3. Create your keys on the [API Keys page](https://developer.stockx.com/portal/keys/).
4. Set up your application in the [Applications section](https://developer.stockx.com/portal/applications/).
5. Populate the `.env` file with your credentials.

---

## Usage
To retrieve your API tokens:

1. Run the `main.py` script:
   ```bash
   python main.py
   ```

2. The script will:
   - Start a local Flask server to handle the OAuth callback.
   - Generate an authorization URL and open it in your default browser.
   - Wait for you to authenticate and authorize the application.
   - Retrieve and save the tokens locally.

3. After successfully retrieving tokens, the script will print:
   ```
   Successfully retrieved tokens
   ```

4. Use the `tokens` object to make authenticated API calls. See the [StockX API Reference](https://developer.stockx.com/openapi/reference/overview/) for available endpoints.

```python
# Example placeholder for API functionality
# args to pass to the API function: tokens, config
perform_some_stockx_api_functionality(tokens, config)
```

---

## Files Overview
- **`main.py`**: The entry point for the script.
- **`auth_flow/`**: Contains the `get_tokens` function for handling the authentication process.
- **`utils/`**:
  - `config_loader.py`: Loads the environment variables from the `.env` file.
  - Other utilities for handling token management.
- **`.env`**: Template for your StockX API credentials.
- **`requirements.txt`**: List of dependencies required to run the project.

---

## Notes
- Ensure your `REDIRECT_URI` matches the callback URL configured in your StockX application settings.
- The Flask server uses SSL for secure communication. Make sure `cert.pem` and `key.pem` are properly generated and available in the project root.
- Tokens are saved locally for reuse but ensure proper security measures when handling them.
- Refer to the [StockX API Reference](https://developer.stockx.com/openapi/reference/overview/) for details on making API calls.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

For more details on the StockX API, refer to the [official documentation](https://developer.stockx.com/).

