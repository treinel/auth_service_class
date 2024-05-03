
from jwt import encode, decode

def encode_jwt(data:dict):
    token: str = encode(payload=data, key="my_secret_key", algorithm='HS256')
    return token

def decode_jwt(token:str) -> dict:
    data: dict = decode(jwt=token, key="my_secret_key", algorithms=['HS256'])
    return data

