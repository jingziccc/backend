> pip install fastapi
> pip install "uvicorn[standard]”
> 
> uvicorn main:app --reload
>
# backend

## 配置开发环境
### 安装依赖
+ pip install fastapi
+ pip install "uvicorn[standard]”
+ pip install tortoise-orm
+ 
### 配置orm
+ aerich init -t database.config.CONFIG # 初始化配置文件
+ aerich init-db # 初始化数据库, 一般在第一次使用时执行
+ aerich migrate [--name] (标记修改操作) #  更新操作并生成迁移文件
+ aerich upgrade # 更新数据库
+ aerich downgrade # 回滚数据库
+ aerich history # 查看历史操作

### 配置身份验证


### 查看swagger
> http://127.0.0.1:8000/docs