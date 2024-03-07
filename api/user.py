from fastapi import APIRouter, Depends, HTTPException, Form, status
from database.models import User
from fastapi.security import OAuth2PasswordRequestForm
from tools.security import get_password_hash, create_access_token, authenticate_user, get_current_user, Token
from common.CommonResponse import CommonResponse

userAPI = APIRouter()


@userAPI.get("/current_user")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@userAPI.post("/token")
async def login_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=await create_access_token(data={"sub": user.username}), token_type="bearer")


@userAPI.post("/register")
async def register(username: str = Form(), password: str = Form(), email: str = Form(), phone: str = Form(), role: int = Form(), avatar: str = Form()):
    if await User.exists(username=username):
        return CommonResponse.error(120, "用户名已存在")
    hashed_password = get_password_hash(password)
    user = await User.create(username=username, hashed_password=hashed_password, email=email, phone=phone, role=role, avatar=avatar)
    return Token(access_token=await create_access_token(data={"sub": user.username}), token_type="bearer")


@userAPI.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=await create_access_token(data={"sub": user.username}), token_type="bearer")
