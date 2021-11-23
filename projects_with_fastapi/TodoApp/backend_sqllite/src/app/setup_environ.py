import os


def configure_environment():
    SQLALCHEMY_DB_URL = os.environ.get('SQLALCHEMY_DB_URL')
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')

    def get_keys():
        return SQLALCHEMY_DB_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

    return get_keys()
