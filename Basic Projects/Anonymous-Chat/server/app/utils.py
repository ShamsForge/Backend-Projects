from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(stored_chats: str):
    return pwd_context.hash(stored_chats)


def verify(secret, hashed_secret):
    return pwd_context.verify(secret, hashed_secret)
