import subprocess

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status, Depends
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import shutil
import hashlib
import os
from pathlib import Path
from databases import Database
from subprocess import CompletedProcess

DATABASE_URL = "mysql://tzb:6zinnjSCChXFH647@111.229.169.56:3306/tzb"
database = Database(DATABASE_URL)
uploaded_files_md5s = {}


class Item(BaseModel):
    data: str


class PieData(BaseModel):
    value: float
    name: str


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
            # 即：machine_name_component_name_component_type_owner_life_filename
            parts = file.stem.split("_")  # 使用 stem 获取不带扩展名的文件名部分
            if len(parts) >= 5:  # 确保文件名包含足够的部分
                # 将解析的部分组装成一个字典
                file_info = {
                    "machine_name": parts[0],
                    "component_name": parts[1],
                    "component_type": parts[2],
                    "owner": parts[3],
                    "life": int(parts[4]),
                    # 处理文件名中可能包含的额外下划线
                    "filename": "_".join(parts[5:]) + file.suffix
                }
                parsed_files.append(file_info)
            else:
                print(f"File {file.name} does not match the expected pattern.")
    return parsed_files


# 按照machine_name_component_name_component_type_owner_life_filename的格式重新命名文件
def rename_file(file: Path, new_life: int):
    # 分割父级目录和文件名
    parent, filename = os.path.split(file)
    # 重命名文件
    new_filename = f"{file.stem.split('_')[0]}_{file.stem.split('_')[1]}_{file.stem.split(
        '_')[2]}_{file.stem.split('_')[3]}_{new_life}_{file.stem.split('_')[-1]}{file.suffix}"
    new_file = os.path.join(parent, new_filename)
    print(f"Renaming {file} to {new_file}")
    os.rename(file, new_file)


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


@app.post("/upload/", tags=["数据中心"])
async def upload_file(
        file: UploadFile = File(...),
        machine_name: str = Form(...),
        component_name: str = Form(...),
        component_type: str = Form(...),
        owner: str = Form(...)
):
    # 判断目录存在
    path = Path("./uploaded_files")
    if not path.is_dir():
        path.mkdir()
    # 保存文件
    file_location = f"./uploaded_files/{machine_name}_{
        component_name}_{component_type}_{owner}_-1_{file.filename}"
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


@app.get("/dataMsg", tags=["数据中心"])
async def data_msg():
    parsed_files = parse_uploaded_files("./uploaded_files")
    return parsed_files


@app.get("/md5s", tags=["md5"])
async def md5s():
    global uploaded_files_md5s
    if not bool(uploaded_files_md5s):
        uploaded_files_md5s = get_files_md5("./uploaded_files")
    return uploaded_files_md5s


@app.get("/md5/{md5}", tags=["md5"])
async def md5(md5: str):
    global uploaded_files_md5s
    if not bool(uploaded_files_md5s):
        uploaded_files_md5s = get_files_md5("./uploaded_files")
    if md5 in uploaded_files_md5s.values():
        return {"info": "The file exists."}
    else:
        raise HTTPException(status_code=404, detail="File not found.")


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
                rename_file(file, life)
            else:
                return HTTPException(status_code=500, detail=result.stderr)
    return {"info": "Predicted all files.", "result": "success"}


@app.put("/register", tags=["用户中心"])
async def register(name: str, password: str, phone: str):
    await database.execute(
        query="INSERT INTO user (name, password, phone) VALUES (:name, :password, :phone)",
        values={"name": name, "password": password, "phone": phone}
    )
    return {"info": "Register successfully."}


@app.get("/OverviewData")
async def read_chart_data():
    with open("myChart_data.txt", "r") as file:
        data = json.load(file)
        print(data)
    return data


@app.get("/OverviewData/pie1_data.txt")
async def read_pie1_data():
    with open("OverviewData/pie1_data.txt", "r") as file:
        data = json.load(file)
        return [PieData(**item) for item in data]


@app.get("/OverviewData/pie2_data.txt")
async def read_pie1_data():
    with open("OverviewData/pie2_data.txt", "r") as file:
        data = json.load(file)
        return [PieData(**item) for item in data]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
