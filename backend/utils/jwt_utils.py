import jwt
from config import Config
from datetime import datetime, timedelta
from typing import Dict

def create_access_token(data: Dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(seconds=Config.ACCESS_EXPIRES_SECONDS)
    payload["type"] = "access"
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")

def create_refresh_token(data: Dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(seconds=Config.REFRESH_EXPIRES_SECONDS)
    payload["type"] = "refresh"
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")

def decode_token(token: str):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise
    except Exception as e:
        raise
