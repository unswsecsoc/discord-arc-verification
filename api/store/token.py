import jwt
import config
import time
import base64

import lib.const as const
import lib.redis

EXPIRES_VERIFICATION = 3600
EXPIRES_VALIDATION = 3600

AUD_VERIFICATION = "verification"
AUD_VALIDATION = "validation"

def generate(audience: str, expires: int, data: object):
  encoded = jwt.encode({
    **data,
    "iss": "api",
    "aud": audience,
    "exp": int(time.time()) + expires
    }, config.jwt_secret, algorithm="HS256").decode("utf-8")
  return encoded

def generate_verification(uid: str, gid: str):
  return generate(AUD_VERIFICATION, EXPIRES_VERIFICATION, {
    "uid": uid,
    "gid": gid
  })

def generate_validation(uid: str, typ: str):
  return generate(AUD_VALIDATION, EXPIRES_VALIDATION, {
    "uid": uid,
    "typ": typ
  })


def validate(audience: str, token: str):
  # try to decode
  try:
    decoded = jwt.decode(token, config.jwt_secret, audience=audience, algorithm="HS256")

    # if decode successful, check if sig is already in store
    signature = token.split('.')[2]
    if lib.redis.conn.exists(const.TOKEN_PREFIX + signature):
      return None

    return decoded
  except jwt.exceptions.InvalidTokenError as e:
    return None

"""
Validate and destroy token, only consumes one round trip to redis.
"""
def validate_destroy(audience: str, token: str):
  try:
    decoded = jwt.decode(token, config.jwt_secret, audience=audience, algorithm="HS256")

    # if decode successful, check if sig is already in store

    signature = token.split('.')[2]

    # +2 in case of NTP syncing issues
    if "exp" in decoded:
      res = lib.redis.conn.set(
        const.TOKEN_PREFIX + signature, 
        b'1', ex=decoded["exp"] + 2 - int(time.time()),
        nx=True
      )
      if not res:
        return None

    return decoded
  except jwt.exceptions.InvalidTokenError as e:
    return None

def destroy(token: str):
  # doesn't really matter here, always be sure to validate before destroying
  try:
    decoded = jwt.decode(token, verify=False)
    signature = token.split('.')[2]
    
    # destroy actually creates an entry in redis, what a coincidence!
    # +2 in case of NTP syncing issues
    if "exp" in decoded:
      res = lib.redis.conn.set(
        const.TOKEN_PREFIX + signature, 
        b'1', ex=decoded["exp"] + 2 - int(time.time()),
        nx=True
      )
      if not res:
        return False

    return True
  except jwt.exceptions.InvalidTokenError:
    return False