from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def get_password_hash(pwd: str) -> str:
        return pwd_cxt.hash(pwd)

    def verify_password(hashed_password: str, plain_password: str) -> str:
        return pwd_cxt.verify(plain_password, hashed_password)
