from hashlib import sha256
import secrets

def crypto_hash(token: str):
    h = sha256()
    h.update(token.encode('ascii'))
    return h.digest()

def random_token():
    return secrets.token_urlsafe(32)