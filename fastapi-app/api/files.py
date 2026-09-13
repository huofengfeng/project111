import os
import uuid
import shutil

from fastapi import APIRouter, Depends, UploadFile, File

from common.result import Result
from utils.auth import require_admin

UPLOAD_DIR = "files"
router = APIRouter(prefix="/files")


# 文件上传（需要登录）
@router.post("/upload")
async def upload_file(file: UploadFile = File(...), current_user=Depends(require_admin)):
    """上传单个文件，返回可通过静态服务访问的 URL"""
    # 确保上传目录存在
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # 生成唯一文件名，避免冲突
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_location = os.path.join(UPLOAD_DIR, unique_name)

    # 保存文件
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 返回静态文件服务 URL
    return Result.success(f"/uploads/{unique_name}")
