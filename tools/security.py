from datetime import datetime, timedelta, timezone
from typing import Union
from passlib.context import CryptContext
from typing import Union
from database.models import User
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
SECRET_KEY = "7e93a0a11669ba8adeb21097daf302569bad252992cc1c2bf929f606b2be23f045575c790b18f1ba41be715a6a2ce833c894d78da1a40ea7ac44b5cbefd98e25"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


class Token(BaseModel):
    access_token: str
    token_type: str

    def __str__(self):
        return f"access_token: {self.access_token}, token_type: {self.token_type}"

class TokenData(BaseModel):
    username: Union[str, None] = None


def get_oauth2_scheme():
    return oauth2_scheme


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    try:
        user = await User.get(username=username)
    except:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException
    {
        "detail": "Could not validate credentials",
        "headers": {"WWW-Authenticate": "Bearer"},
        "status_code": status.HTTP_401_UNAUTHORIZED
    }
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await User.get(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
