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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
