from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import httpx
import jwt
from jwt import PyJWKSet
import logging
from app.schemas.tokendata import TokenData
from app.config import settings

security = HTTPBearer()

JWT_AUDIENCE = settings.jwt_audience
JWT_ISSUER = settings.jwt_issuer
JWKS_URL = settings.jwks_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_jwks():
    try:
        with httpx.Client() as client:
            response = client.get(JWKS_URL, timeout=10)
            response.raise_for_status()
            jwks_data = response.json()
            return PyJWKSet.from_dict(jwks_data)
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTPStatusError: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def get_signing_key_from_jwks(jwks, kid):
    for key in jwks.keys:
        print(key)
        if key.key_id == kid:
            return key.key
    raise HTTPException(status_code=401, detail="Signing key not found")


def verify_token(token: str):
    try:
        jwks = get_jwks()
        header = jwt.get_unverified_header(token)
        logger.debug(f"header: {header}")
        # signing_key = jwks_client.get_signing_key(header["kid"]).key
        signing_key = get_signing_key_from_jwks(jwks, header["kid"])
        print(signing_key)
        logger.debug(f"signing_key: {signing_key}")

        payload = jwt.decode(
            token,
            signing_key,
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
            algorithms=["RS256"],
        )
        logger.debug(f"payload: {payload}")
        roles = []
        resource_access = payload.get("resource_access", {})
        for resource_name, resource in resource_access.items():
            if resource_name == "springboot":
                roles.extend(resource.get("roles", []))
        return TokenData(
            name=payload["name"],
            preferred_username=payload["preferred_username"],
            sub=payload["sub"],
            email=payload["email"],
            roles=roles,
        )
    except jwt.PyJWTError as e:
        logger.error(f"PyJWTError: {e}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    except Exception as e:
        logger.error(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    return verify_token(credentials.credentials)


def require_roles(required_roles: list):
    def role_checker(user: TokenData = Depends(get_current_user)):
        if not set(required_roles).intersection(set(user.roles)):
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user

    return role_checker
