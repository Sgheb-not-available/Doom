from cryptography.fernet import Fernet
import base64, hashlib

def get_fernet(password: str):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

def encrypt(text: str, password: str) -> str:
    return get_fernet(password).encrypt(text.encode()).decode()

def decrypt(text: str, password: str) -> str:
    return get_fernet(password).decrypt(text.encode()).decode()