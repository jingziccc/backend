from fastapi import APIRouter, Form, UploadFile, Depends, HTTPException
from database.models import MModel, User, Component
from tools.security import get_current_user
from typing import Optional

componentAPI = APIRouter()


@componentAPI.post("/upload")
async def upload_component(
    name: str = Form(...),
    location: str = Form(...),
    model: Optional[int] = Form(None),
    pic: UploadFile = Form(...),
    current_user: User = Depends(get_current_user)
):
    if model is None:
        component = await Component.create(
            name=name,
            location=location,
            user=current_user,
            pic=await pic.read()
        )
    else:
        model = await MModel.get(id=model)
        if not model:
            raise HTTPException(status_code=400, detail="模型不存在")
        component = await Component.create(
            name=name,
            location=location,
            model=model,
            user=current_user,
            pic=await pic.read()
        )
    return component


@componentAPI.get("/all_user")
async def read_user_components(current_user: User = Depends(get_current_user)):
    return await Component.filter(user=current_user)

# 返回当前用户下各模型的组件数量


@componentAPI.get("/model_count")
async def read_model_count(current_user: User = Depends(get_current_user)):
    component = await Component.filter(user=current_user)
    model_count = {}
    for c in component:
        if c.name in model_count:
            model_count[c.name] += 1
        else:
            model_count[c.name] = 1
    return model_count
