from datetime import datetime, timedelta
from pydantic import EmailStr

from app.core.config import JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.core import CoreModel


class JWTMeta(CoreModel):
    iss: str = "phresh.io"                              # issuer of token
    aud: str = JWT_AUDIENCE                             # who token is intended for
    iat: float = datetime.timestamp(datetime.utcnow())  # when token was issued at
    exp: float = datetime.timestamp(datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))  # when token was expires


class JWTCreds(CoreModel):
    """ How we idenitify users """
    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    """JWT payload before encoding - meta + username"""
    pass


class AccessToken(CoreModel):
    access_token: str
    token_type: str
