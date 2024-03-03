from fastapi import APIRouter, Form, UploadFile, Depends, HTTPException
from database.models import MModel, User
from tools.security import get_current_user
from tools.md5 import get_file_md5

modelAPI = APIRouter()


@modelAPI.get("/all")
async def read_models():
    return await MModel.all()


@modelAPI.post("/", response_model_exclude={"model_file"})
async def create_model(model_file: UploadFile, name: str = Form(), style: str = Form(), status: str = Form(), description: str = Form(), _: User = Depends(get_current_user)):
    # 检查模型名是否重复
    if await MModel.exists(name=name):
        raise HTTPException(status_code=400, detail="模型名已存在")
    md5 = await get_file_md5(model_file)
    if await MModel.exists(md5=md5):
        raise HTTPException(status_code=400, detail="模型文件已存在")
    model = await MModel.create(name=name, style=style, status=status, description=description, model_file=model_file.file.read(), md5=md5)
    # 将模型文件存储到本地
    with open(f"./model_files/{md5}", "wb") as f:
        f.write(model.model_file)
    return model


@modelAPI.get("/style", description="获取各模型风格占百分比", tags=["charts"])
async def style():
    style = await MModel.all().values_list('style', flat=True)
    total = len(style)
    style_dict = {}
    for s in style:
        if s in style_dict:
            style_dict[s] += 1
        else:
            style_dict[s] = 1
    for k in style_dict:
        style_dict[k] /= total
    return style_dict


@modelAPI.get("/status", description="获取各模型状态占百分比", tags=["charts"])
async def status():
    status = await MModel.all().values_list('status', flat=True)
    total = len(status)
    status_dict = {}
    for s in status:
        if s in status_dict:
            status_dict[s] += 1
        else:
            status_dict[s] = 1
    for k in status_dict:
        status_dict[k] /= total
    return status_dict
