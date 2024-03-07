from fastapi import APIRouter, Form, UploadFile, Depends, HTTPException
from database.models import MModel, User, Component
from tools.security import get_current_user
from typing import Union
from common.CommonResponse import CommonResponse

componentAPI = APIRouter()


@componentAPI.post("/upload", response_model_exclude={"pic", "model", "user"})
async def upload_component(
    pic: UploadFile,
    name: str = Form(...),
    location: str = Form(...),
    model: Union[int, None] = Form(...),
    current_user: User = Depends(get_current_user)
):
    # 检查组件名是否重复
    if await Component.exists(name=name, user=current_user):
        return CommonResponse.error(110, "组件名已存在")

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
            return CommonResponse.error(103, "模型不存在")
        component = await Component.create(
            name=name,
            location=location,
            model=model,
            user=current_user,
            pic=await pic.read()
        )
    component.model = ''
    component.pic = ''
    return component


@componentAPI.get("/all_user")
async def read_user_components(current_user: User = Depends(get_current_user)):
    return await Component.filter(user=current_user)


@componentAPI.get("/model_count", description="返回当前用户下各模型的组件数量", tags=["charts"])
async def read_model_count(current_user: User = Depends(get_current_user)):
    component = await Component.filter(user=current_user)
    model_count = {}
    for c in component:
        if c.name in model_count:
            model_count[c.name] += 1
        else:
            model_count[c.name] = 1
    return model_count


@componentAPI.get("/location_count", description="返回当前用户下各位置的组件数量", tags=["charts"])
async def read_location_count(current_user: User = Depends(get_current_user)):
    component = await Component.filter(user=current_user)
    location_count = {}
    for c in component:
        if c.location in location_count:
            location_count[c.location] += 1
        else:
            location_count[c.location] = 1
    return location_count
