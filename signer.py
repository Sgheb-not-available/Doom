import hmac
import hashlib
import os
import dotenv
import secrets
import keyring

APP_NAME = "doom"
KEY_NAME = "secret_key"

def get_secret_key() -> str:
    dotenv.load_dotenv()
    env_key = os.getenv("DOOM_SECRET")
    if env_key:
        return env_key
    
    key = keyring.get_password(APP_NAME, KEY_NAME)
    
    if not key:
        key = secrets.token_hex(32)
        keyring.set_password(APP_NAME, KEY_NAME, key)
    
    return key

SECRET_KEY = get_secret_key()

def sign_data(data: str) -> str:
    return hmac.new(SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()

def verify_signature(data: str, signature: str) -> bool:
    expected = sign_data(data)
    return hmac.compare_digest(expected, signature)