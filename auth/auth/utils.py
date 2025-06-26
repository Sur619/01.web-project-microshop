import jwt
from core.config import AuthJWT


def encode_jwt(
    payload,
    key,
    algorithm,
):
    encoded = jwt.encode(
        payload,
        key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token,
    public_key,
    algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
