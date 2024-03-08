from fastapi import APIRouter, Form, Depends
from database.models import Component, User
from tools.security import get_current_user

componentAPI = APIRouter()


@componentAPI.post("/upload")
async def upload(name: str = Form(), location: str = Form(), user: User = Depends(get_current_user)):
    component = await Component.create(name=name, location=location, user=user)
    return component
