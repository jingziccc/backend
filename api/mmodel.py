from fastapi import APIRouter, Form, UploadFile, Depends, HTTPException, File
from database.models import MModel, User
from tools.security import get_current_user
from tools.md5 import get_file_md5
from common.CommonResponse import CommonResponse
import os

modelAPI = APIRouter()


@modelAPI.get("/all")
async def read_models():
    return await MModel.all()


@modelAPI.post("/", response_model_exclude={"modelfile"})
async def create_model(modelfile: UploadFile, name: str = Form(), style: str = Form(), status: str = Form(), description: str = Form(), _: User = Depends(get_current_user)):
    # 检查是否是合法的模型文件
    # TODO

    # 检查模型名是否重复
    file_content = await modelfile.read()
    if await MModel.exists(name=name):
        return CommonResponse.error(100, "模型名已存在")
    md5 = await get_file_md5(file_content)
    if await MModel.exists(md5=md5):
        return CommonResponse.error(101, "模型文件已存在")
    model = await MModel.create(name=name, style=style, status=status, description=description, modelfile=file_content, md5=md5)
    # 将模型文件存储到本地
    # 如果目录不存在则创建
    if not os.path.exists("./model_files"):
        os.makedirs("./model_files")
    with open(f"./model_files/{md5}", "wb") as f:
        f.write(file_content)
    model.modelfile = ''
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
    return CommonResponse.success(style_dict)


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

# 获取指定id的模型


@modelAPI.get("/{id}")
async def read_model(id: int):
    model = await MModel.get(id=id)
    # 下载模型文件到d盘
    if not os.path.exists("D:/model_files"):
        os.makedirs("D:/model_files")
    with open(f"D:/model_files/{model.md5}", "wb") as f:
        f.write(model.modelfile)
    if not model:
        return CommonResponse.error(103, "模型不存在")
    return model
