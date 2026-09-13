from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import BaseModel
import os
import uuid
import shutil

from common.exception_handler import CustomException
from common.result import Result
from models import Admin, User
from utils.auth import get_current_user

router = APIRouter(prefix="/profile", dependencies=[Depends(get_current_user)])
UPLOAD_DIR = "files"


class ProfileUpdate(BaseModel):
    name: str = None
    avatar: str = None


@router.get("")
async def get_profile(current_user=Depends(get_current_user)):
    """获取当前登录用户的个人信息（不含密码）"""
    return Result.success({
        "id": current_user.id,
        "username": current_user.username,
        "name": current_user.name,
        "avatar": current_user.avatar,
        "role": current_user.role,
    })


@router.put("")
async def update_profile(data: ProfileUpdate, current_user=Depends(get_current_user)):
    """更新当前用户的名称和头像"""
    update_data = {}
    if data.name is not None:
        update_data["name"] = data.name
    if data.avatar is not None:
        update_data["avatar"] = data.avatar

    if not update_data:
        raise CustomException("没有需要更新的数据")

    if isinstance(current_user, Admin):
        await Admin.filter(id=current_user.id).update(**update_data)
    else:
        await User.filter(id=current_user.id).update(**update_data)

    return Result.success()


@router.post("/avatar")
async def upload_avatar(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    """上传头像，返回可访问的 URL"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    if ext.lower() not in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
        raise CustomException("仅支持 jpg、png、gif、webp 格式的图片")

    unique_name = f"avatar_{uuid.uuid4().hex}{ext}"
    file_location = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    avatar_url = f"http://127.0.0.1:9090/uploads/{unique_name}"

    # 自动更新用户头像
    if isinstance(current_user, Admin):
        await Admin.filter(id=current_user.id).update(avatar=avatar_url)
    else:
        await User.filter(id=current_user.id).update(avatar=avatar_url)

    return Result.success(avatar_url)