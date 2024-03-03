import subprocess
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status, Depends
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

import hashlib
import os
from pathlib import Path
from subprocess import CompletedProcess
from tortoise.contrib.fastapi import register_tortoise
from database.config import CONFIG

from database.models import User
from tools.security import get_current_user


from api.user import userAPI
from api.mmodel import modelAPI
from api.component import componentAPI

uploaded_files_md5s = {}


class Item(BaseModel):
    data: str


class PieData(BaseModel):
    value: float
    name: str


app = FastAPI()
register_tortoise(app=app,
                  config=CONFIG,
                  generate_schemas=True,  # 是否自动生成表结构
                  )
app.include_router(userAPI, prefix="/user", tags=["用户相关API"])
app.include_router(modelAPI, prefix="/model", tags=["模型相关API"])
app.include_router(componentAPI, prefix="/component", tags=["组件相关API"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/current_user")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user



@app.post("/predict")
async def predict(item: Item):
    return {"data": item.data + " accept"}




@app.get("/predict/all", tags=["数据中心"])
async def predict_all():
    # 遍历uoloaded_files目录下的所有xlsx文件
    result: CompletedProcess
    for file in Path("./uploaded_files").iterdir():
        if file.is_file() and file.suffix == ".xlsx":
            # 如果寿命不为-1，则执行命令
            parts = file.stem.split("_")
            if parts[4] != "-1":
                continue
            command = ["python", "./algorithm/random_life.py",
                       "./uploaded_files/" + file.name]
            # 执行命令
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout)
                life = int(result.stdout)
                # 重命名文件
                # 解除占用
                # rename_file(file, life)
            else:
                return HTTPException(status_code=500, detail=result.stderr)
    return {"info": "Predicted all files.", "result": "success"}




@app.get("/OverviewData")
async def read_chart_data():
    with open("myChart_data.txt", "r") as file:
        data = json.load(file)
        print(data)
    return data



@app.get("/OverviewData/pie2_data.txt")
async def read_pie1_data():
    with open("OverviewData/pie2_data.txt", "r") as file:
        data = json.load(file)
        return [PieData(**item) for item in data]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
