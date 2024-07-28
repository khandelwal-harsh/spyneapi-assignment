import datetime

import jwt
from django.conf import settings
from django.utils import timezone

# TODO: make configurable and change algorithm
ALGO = "HS256"
EXPIRE_DAYS = 3


def encode(data: dict) -> str:
    data["exp"] = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(
        days=EXPIRE_DAYS
    )
    return jwt.encode(data, settings.SECRET_KEY, algorithm=ALGO)


def decode(encoded_jwt: str) -> dict:
    return jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=[ALGO])
