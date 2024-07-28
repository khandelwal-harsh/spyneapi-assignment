from dataclasses import dataclass

import jwt
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication, exceptions

from spyneai.jwt import decode

@dataclass(frozen=True)
class TokenData:
    key: str


class BearerAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate_credentials(self, key):
        try:
            token_data = decode(key)
            key = token_data.get("key")
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        model = self.get_model()

        try:
            token = model.objects.using("default").select_related("user").get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))
        print("\n\ntoken", token)
        setattr(token.user, "token_data", token_data)
        return token.user, token