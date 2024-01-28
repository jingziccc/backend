import subprocess

from fastapi import FastAPI, File, UploadFile, Form, HTTPException,status,Depends
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import hashlib
import os
from pathlib import Path
from databases import Database


DATABASE_URL = "mysql://tzb:6zinnjSCChXFH647@111.229.169.56:3306/tzb"
database = Database(DATABASE_URL)
uploaded_files_md5s = {}


class Item(BaseModel):
    data: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def calculate_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def get_files_md5(directory: str):
    md5s = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            md5s[file] = calculate_md5(path)
    return md5s


def parse_uploaded_files(directory: str):
    # 确保路径存在
    path = Path(directory)
    if not path.is_dir():
        print(f"The directory {directory} does not exist.")
        return []

    # 存储解析结果的列表
    parsed_files = []
    # 遍历目录下的所有文件
    for file in path.iterdir():
        if file.is_file():
            # 分解文件名，这里假设文件名的格式严格遵循给定的模式
            # 即：machine_name_component_name_component_type_owner_filename
            parts = file.stem.split("_")  # 使用 stem 获取不带扩展名的文件名部分
            if len(parts) >= 5:  # 确保文件名包含足够的部分
                # 将解析的部分组装成一个字典
                file_info = {
                    "machine_name": parts[0],
                    "component_name": parts[1],
                    "component_type": parts[2],
                    "owner": parts[3],
                    "life": int(parts[4]),
                    "filename": "_".join(parts[5:]) + file.suffix  # 处理文件名中可能包含的额外下划线
                }
                parsed_files.append(file_info)
            else:
                print(f"File {file.name} does not match the expected pattern.")
    return parsed_files


@app.get("/modelMsg")
async def model_msg():
    return {
        "0001": {
            "模型风格": "model1",
            "模型类型": "ResNet50",
            "算法名称": 0.9,
            "训练情况": 0.8,
            "创建时间": 2024 - 12 - 12,
        },
        "0002": {
            "模型风格": "model2",
            "模型类型": "Transformer",
            "算法名称": 0.9,
            "训练情况": 0.8,
            "创建时间": 2024 - 12 - 12,
        },
        "0003": {
            "模型风格": "model3",
            "模型类型": "TimeGPT",
            "算法名称": 0.9,
            "训练情况": 0.8,
            "创建时间": 2024 - 12 - 12,
        }
    }


@app.post("/predict")
async def predict(item: Item):
    return {"data": item.data + " accept"}


@app.post("/upload/")
async def upload_file(
        file: UploadFile = File(...),
        machine_name: str = Form(...),
        component_name: str = Form(...),
        component_type: str = Form(...),
        owner: str = Form(...)
):
    file_location = f"./uploaded_files/{machine_name}_{component_name}_{component_type}_{owner}_-1_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # 计算md5
    uploaded_files_md5s[file.filename] = calculate_md5(file_location)
    return {
        "filename": file.filename,
        "machine_name": machine_name,
        "component_name": component_name,
        "component_type": component_type,
        "owner": owner,
        "life": -1,
        "info": "File saved successfully."
    }


@app.get("/dataMsg")
async def data_msg():
    parsed_files = parse_uploaded_files("./uploaded_files")
    return parsed_files


@app.get("/md5s")
async def md5s():
    global uploaded_files_md5s
    if not bool(uploaded_files_md5s):
        uploaded_files_md5s = get_files_md5("./uploaded_files")
    return uploaded_files_md5s


@app.get("/md5/{md5}")
async def md5(md5: str):
    global uploaded_files_md5s
    if not bool(uploaded_files_md5s):
        uploaded_files_md5s = get_files_md5("./uploaded_files")
    if md5 in uploaded_files_md5s.values():
        return {"info": "The file exists."}
    else:
        raise HTTPException(status_code=404, detail="File not found.")


@app.get("/predict/all")
async def predict_all():
    # subprocess.Popen('python ./algorithm/pre.py ' + './uploaded_files/测试机_发动机2_发动机_李峰_-1_N-CMAPSS_DS08c-008.h5',
    #                  shell=True)
    # subprocess.Popen(
    #     'python ./algorithm/data_deal.py ' + './uploaded_files/测试机_发动机2_发动机_李峰_-1_N-CMAPSS_DS08c-008.h5',
    #     shell=True)
    return {"info": "Predict all files."}


@app.put("/register")
async def register(name: str, password: str, phone: str):

    await database.execute(
        query="INSERT INTO user (name, password, phone) VALUES (:name, :password, :phone)",
        values={"name": name, "password": password, "phone": phone}
    )
    return {"info": "Register successfully."}
