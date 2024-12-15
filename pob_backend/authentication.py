from rest_framework.authentication import (
    TokenAuthentication,
    get_authorization_header,
)
from rest_framework.exceptions import AuthenticationFailed
import requests
import jwt
import json
from jwt.exceptions import InvalidTokenError
from jwt.algorithms import RSAAlgorithm
from django.conf import settings
from rest_framework import authentication
from django.contrib.auth import get_user_model
from functools import lru_cache
from constance import config

User = get_user_model()


@lru_cache(maxsize=1)
def get_keycloak_public_key():
    """Fetch and cache the Keycloak public key"""
    base_url = config.KEYCLOAK_BASE_URL
    realm = config.KEYCLOAK_REALM
    issuer = f"{base_url}/realms/{realm}"
    jwks_uri = f"{issuer}/protocol/openid-connect/certs"

    response = requests.get(jwks_uri)
    if response.status_code == 200:
        jwks = response.json()
        if "keys" in jwks:
            # Find key with alg RS256
            for key in jwks["keys"]:
                if key.get("alg") == "RS256":
                    return RSAAlgorithm.from_jwk(json.dumps(key))
    return None


class CustomTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request).decode("utf-8")

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2:
            return None

        token_type = parts[0]
        token = parts[1]

        # Check if it's a DRF token
        if token_type == "Token":
            try:
                drf_auth = TokenAuthentication()
                return drf_auth.authenticate(request)
            except AuthenticationFailed:
                pass

        # Check if it's a Bearer token (Keycloak)
        elif token_type == "Bearer":
            try:
                public_key = get_keycloak_public_key()
                if not public_key:
                    raise AuthenticationFailed("Unable to verify token")

                # Verify and decode the JWT
                decoded_token = jwt.decode(
                    token,
                    public_key,
                    algorithms=["RS256"],
                    audience=config.KEYCLOAK_CLIENT_ID,
                    issuer=f"{config.KEYCLOAK_BASE_URL}/realms/{config.KEYCLOAK_REALM}",
                )

                # Get user info from token
                email = decoded_token.get("email")
                print(email)
                if not email:
                    raise AuthenticationFailed("Email not found in token")

                try:
                    user = User.objects.get(email=email)
                    return (user, None)
                except User.DoesNotExist:
                    raise AuthenticationFailed("User not found")

            except InvalidTokenError as e:
                raise AuthenticationFailed(f"Invalid token: {str(e)}")
            except Exception as e:
                raise AuthenticationFailed(f"Authentication failed: {str(e)}")

        raise AuthenticationFailed("Invalid token")
