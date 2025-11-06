from datetime import timedelta, datetime
import os
from jose import jwt
from model.schemas.user import User
from data import user as data


from passlib.context import CryptContext

SECRET_KEY = "Keep-it-safe-and-secret"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hash: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain, hash)

def get_hash(plain:str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(plain)

def get_jwt_username(token: str) -> str | None:
    """Extract username from JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get("sub")):
            return None
    except jwt.JWTError:
        return None
    return username

def get_current_user(token: str) -> User | None:
    """Get current user from JWT token"""
    if not (username := get_jwt_username(token)):
        return None
    if (user := lookup_user(username)) is None:
        return None
    return user

def lookup_user(name: str) -> User | None:
    """Lookup user by name"""
    if (user := data.get_one(name)):
        return user
    return None

def auth_user(name: str, plain: str) -> User | None:
    """Authenticate user by name and password"""
    if not (user := lookup_user(name)):
        return None
    if not verify_password(plain, user.hash):
        return None
    return user

def create_access_token(data: dict, expires: timedelta | None = None) -> str:
    """return a JWT access token"""
    src = data.copy()
    now = datetime.utcnow()

    if not expires:
        expires = timedelta(minutes=15)
    
    src.update({"exp": now + expires})
    encoded_jwt = jwt.encode(src, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create(user: User) -> User:
    hashed_user = User(name=user.name, hash=get_hash(user.hash))
    return data.create(hashed_user)