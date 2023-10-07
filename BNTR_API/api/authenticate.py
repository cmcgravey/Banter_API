"""Function for authenticating user info."""
import BNTR_API
import uuid
import hashlib

def verify_key(api_key):
    """Verify API Key."""
    if api_key == BNTR_API.app.config['API_KEY']:
        return True
    else:
        return False
    
def hash_password(password):
    """Hash user's password for database storage."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string

def verify_password(password, userinput):
    """Verify user's password."""
    password = password.split('$')
    algorithm = password[0]
    salt = password[1]
    hash_obj = hashlib.new(algorithm)
    input_w_salt = salt + userinput
    hash_obj.update(input_w_salt.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    if password_hash == password[2]:
        return True
    return False