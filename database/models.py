from tortoise.models import Model
from tortoise import fields


class User(Model):
    username = fields.CharField(pk=True, max_length=50, description="用户名")
    hashed_password = fields.CharField(max_length=128, description="密码")
    email = fields.CharField(max_length=50, description="邮箱")
    phone = fields.CharField(max_length=50, description="电话")
    role = fields.IntField(description="角色")
    avatar = fields.CharField(max_length=1023, description="头像")


class MModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, description="模型名称")
    style = fields.CharField(max_length=50, description="模型风格")
    uploaded_time = fields.DatetimeField(auto_now_add=True, description="上传时间")
    status = fields.IntField(description="训练状态")
    description = fields.TextField(description="描述")


class Component(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, description="组件名称")
    status = fields.IntField(description="组件状态")
    life_forecast = fields.IntField(description="寿命预测")
    location = fields.CharField(max_length=50, description="位置")
    updated_time = fields.DatetimeField(auto_now_add=True, description="更新时间")
    model = fields.ForeignKeyField(
        'models.MModel', related_name='components', description="模型")
    user = fields.ForeignKeyField(
        'models.User', related_name='components', description="用户")
