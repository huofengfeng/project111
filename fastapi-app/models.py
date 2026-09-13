from tortoise.models import Model
from tortoise import fields


class Admin(Model):
    id = fields.IntField(pk=True, null=False)
    username = fields.CharField(max_length=255, null=True)
    password = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255, null=True)
    avatar = fields.CharField(max_length=255, null=True)
    role = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'admin'

class Artifacts(Model):
    id = fields.IntField(pk=True, null=False)
    name = fields.CharField(max_length=255, null=True)
    era = fields.CharField(max_length=255, null=True)
    type = fields.CharField(max_length=255, null=True)
    size = fields.CharField(max_length=255, null=True)
    glaze = fields.CharField(max_length=255, null=True)
    source = fields.CharField(max_length=255, null=True)
    museum = fields.CharField(max_length=255, null=True)
    level = fields.CharField(max_length=255, null=True)
    image_url = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(null=True)
    updated_at = fields.DatetimeField(null=True)

    class Meta:
        table = 'artifacts'



class Tombs(Model):
    id = fields.IntField(pk=True, null=False)
    name = fields.CharField(max_length=100, null=False, description='墓葬名称')
    era = fields.CharField(max_length=50, null=True, description='年代')
    location = fields.CharField(max_length=100, null=True, description='出土地点')
    longitude = fields.FloatField(null=True, description='经度')
    latitude = fields.FloatField(null=True, description='纬度')
    sancai_items = fields.CharField(max_length=200, null=True, description='三彩器物')
    total_items = fields.CharField(max_length=50, null=True, description='出土器物总数')
    created_at = fields.DatetimeField(null=True)
    updated_at = fields.DatetimeField(null=True)

    class Meta:
        table = 'tombs'

class Types(Model):
    id = fields.IntField(pk=True, null=False)
    name = fields.CharField(max_length=100, null=False, description='类型名称')
    category = fields.CharField(max_length=50, null=True, description='大类分类')
    created_at = fields.DatetimeField(null=True)
    updated_at = fields.DatetimeField(null=True)

    class Meta:
        table = 'artifact_types'


class User(Model):
    id = fields.BigIntField(pk=True, null=False)
    username = fields.CharField(max_length=50, null=False, description='用户名')
    password = fields.CharField(max_length=255, null=False, description='bcrypt密码哈希')
    name = fields.CharField(max_length=100, null=True, description='昵称/显示名')
    avatar = fields.CharField(max_length=255, null=True, description='头像URL')
    role = fields.CharField(max_length=50, null=False, default='User', description='角色：User/Admin')

    class Meta:
        table = 'user'


class Favorites(Model):
    id = fields.IntField(pk=True, null=False)
    user_id = fields.BigIntField(null=False, description='用户ID')
    artifact_id = fields.IntField(null=False, description='文物ID')
    created_at = fields.DatetimeField(null=True, auto_now_add=True)

    class Meta:
        table = 'favorites'
        unique_together = (('user_id', 'artifact_id'),)