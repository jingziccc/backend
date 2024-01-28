from fastapi import FastAPI, File, UploadFile, Form,HTTPException
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import hashlib
import os
from pathlib import Path

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
