"""Function for authenticating user."""
import BNTR_API

def verify_key(api_key):
    if api_key == BNTR_API.app.config['API_KEY']:
        return True
    else:
        return False