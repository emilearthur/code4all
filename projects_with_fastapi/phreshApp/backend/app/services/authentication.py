from typing import Optional, Type
import bcrypt
from fastapi import HTTPException, status
import jwt

from passlib.context import CryptContext
from datetime import datetime, timedelta

from pydantic.error_wrappers import ValidationError

from app.models.user import UserPasswordUpdate, UserBase
from app.core.config import SECRET_KEY, JWT_ALGORITHM, JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.token import JWTMeta, JWTCreds, JWTPayload

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(BaseException):
    """Custom auth exception that can be modified later on. """
    pass


class AuthService:
    def create_salt_and_hashed_password(self, *, plaintext_password: str) -> UserPasswordUpdate:
        salt = self.generate_salt()
        hashed_password = self.get_password_hash(password=plaintext_password, salt=salt)
        return UserPasswordUpdate(salt=salt, password=hashed_password)

    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()

    def get_password_hash(self, *, password: str, salt: str) -> str:
        return pwd_cxt.hash(password + salt)

    def verify_password(self, *, plain_password: str, salt: str, hashed_password: str) -> bool:
        return pwd_cxt.verify(plain_password + salt, hashed_password)

    def create_access_token_for_user(self, *, user: Type[UserBase],
                                     secret_key: str = str(SECRET_KEY),
                                     audience: str = JWT_AUDIENCE,
                                     expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES,) -> str:
        if not user or not isinstance(user, UserBase):
            return None
        jwt_meta = JWTMeta(aud=audience, iat=datetime.timestamp(datetime.utcnow()),
                           exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),)
        jwt_creds = JWTCreds(sub=user.email, username=user.username)
        token_payload = JWTPayload(**jwt_meta.dict(), **jwt_creds.dict(),)

        access_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)
        return access_token

    def get_username_from_token(self, *, token: str, secret_key: str) -> Optional[str]:
        try:
            decoded_token = jwt.decode(token, str(secret_key), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
            payload = JWTPayload(**decoded_token)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate token credentials.",
                                headers={"WWW-Authenticate": "Bearer"})
        return payload.username
