from auth_flow import get_tokens

from utils.config_loader import load_environment

def main():
    """Main function to orchestrate token retrieval and API calls."""
    config = load_environment()
    tokens = get_tokens(config)

    if tokens:
        print("\nSuccessfully retreived tokens")
    else:
        print("\nFailed to retrieve tokens.")
        return
    
    '''
    perform some functionality with the StockX API
    args to pass to api function: tokens, config
    '''

if __name__ == "__main__":
    main()