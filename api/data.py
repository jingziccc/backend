from fastapi import UploadFile, Form, Depends, Response
from common.CommonResponse import CommonResponse
from tools.security import get_current_user
from fastapi import APIRouter
from database.models import DData, Component
dataAPI = APIRouter()


@dataAPI.post("/", description="上传数据")
async def create_data(file: UploadFile = Form(...), name: str = Form(...), component: int = Form(...), current_user=Depends(get_current_user)):
    component = await Component.get(id=component).prefetch_related('user')
    if not component:
        return CommonResponse.error(104, "组件不存在")
    if component.user != current_user:
        return CommonResponse.error(124, "无权访问其它用户的组件信息")
    data = await DData.create(
        file=await file.read(),
        name=name,
        component=component
    )
    return data


@dataAPI.get("/user_component/{id}", description="返回当前用户下的某个组件的数据")
async def read_user_component_data(id: int, current_user=Depends(get_current_user)):
    component = await Component.get(id=id).prefetch_related('user')
    if not component:
        return CommonResponse.error(104, "组件不存在")
    if component.user != current_user:
        return CommonResponse.error(124, "无权访问其它用户的组件信息")
    datas = await DData.filter(component=component)
    for d in datas:
        d.file = ''
    return datas


@dataAPI.get("/download/{id}", description="下载数据")
async def download_data(id: int, current_user=Depends(get_current_user)):
    data = await DData.get(id=id).prefetch_related('component__user')
    if not data:
        return CommonResponse.error(105, "数据不存在")
    if data.component.user != current_user:
        return CommonResponse.error(125, "无权下载其它用户的数据")
    return Response(content=data.file, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={data.name}"})
