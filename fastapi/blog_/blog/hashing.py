from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcryt(pwd: str) -> str:
        
        return pwd_cxt.hash(pwd)