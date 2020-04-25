from lib.redis import conn
from lib.security import crypto_hash, random_token
from datetime import timedelta
import json

EV_PREFIX = b'ev:'
EXPIRES = timedelta(seconds=3600)

class EmailVerification:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def serialize(self):
        return json.dumps({
            'u': self.user_id
        })

    @classmethod
    def by_token(cls, token):
        token_hash = crypto_hash(token)
        res = conn.get(EV_PREFIX + token_hash)
        if res == None:
            return
        data = json.loads(res)
        return cls(data['u'])

    @classmethod
    def destroy(cls, token):
        token_hash = crypto_hash(token)
        conn.delete(EV_PREFIX + token_hash)
    
    @classmethod
    def create(cls, user_id):
        token = random_token()
        token_hash = crypto_hash(token)
        obj = cls(user_id)
        conn.set(EV_PREFIX + token_hash, obj.serialize(), EXPIRES)
        
        return (token, EXPIRES)
