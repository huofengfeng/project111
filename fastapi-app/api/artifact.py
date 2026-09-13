from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import create_model
from tortoise.contrib.pydantic import pydantic_model_creator

from common.result import Result, PageInfo
from models import Artifacts
from utils.auth import require_admin

router = APIRouter(prefix="/artifact")

ArtifactsPydantic = pydantic_model_creator(Artifacts)

ArtifactsCreatePydantic = create_model(
    "ArtifactsCreatePydantic",
    **{
        name: (Optional[field.annotation], None)
        for name, field in ArtifactsPydantic.model_fields.items()
    }
)


# ====== 字段映射：Artifacts 模型 -> 时间线前端所需字段 ======
def to_timeline_item(a: dict) -> dict:
    """将 Artifacts 模型字段映射为时间线前端所需的字段名"""
    return {
        "id": a.get("id"),
        "name": a.get("name"),
        "dynasty": a.get("era"),
        "excavation_site": a.get("source"),
        "artifact_type": a.get("type"),
        "glaze_color": a.get("glaze"),
        "image_url": a.get("image_url"),
        "museum": a.get("museum"),
    }


# ====== 基础 CRUD ======

@router.post("/add")
async def add(data: ArtifactsCreatePydantic, current_user=Depends(require_admin)):
    create_data = data.model_dump(exclude_unset=True, exclude={'id'})
    await Artifacts.create(**create_data)
    return Result.success()


@router.put("/update")
async def update(data: ArtifactsCreatePydantic, current_user=Depends(require_admin)):
    update_data = data.model_dump(exclude_unset=True, exclude={"id"})
    await Artifacts.filter(id=data.id).update(**update_data)
    return Result.success()


@router.delete("/delete/{artifact_id}")
async def delete(artifact_id: int, current_user=Depends(require_admin)):
    await Artifacts.filter(id=artifact_id).delete()
    return Result.success()


@router.delete("/deleteBatch")
async def delete_batch(ids: List[int], current_user=Depends(require_admin)):
    await Artifacts.filter(id__in=ids).delete()
    return Result.success()


@router.get("/selectById/{artifact_id}")
async def select_one(artifact_id: int):
    artifact = await Artifacts.get_or_none(id=artifact_id)
    if artifact is None:
        from common.exception_handler import CustomException
        raise CustomException("文物不存在")
    data = ArtifactsPydantic.model_validate(artifact).model_dump()
    return Result.success(to_timeline_item(data))


@router.get("/selectAll")
async def select_all(
    name: str = "",
    dynasty: str = "",
    artifact_type: str = "",
    glaze_color: str = "",
):
    query = Artifacts.filter(name__contains=name)
    if dynasty:
        query = query.filter(era__contains=dynasty)
    if artifact_type:
        query = query.filter(type__contains=artifact_type)
    if glaze_color:
        query = query.filter(glaze__contains=glaze_color)

    artifact_list = await query
    artifact_list = [
        to_timeline_item(ArtifactsPydantic.model_validate(a).model_dump())
        for a in artifact_list
    ]
    return Result.success(artifact_list)


@router.get("/selectPage")
async def select_page(
    name: str = "",
    dynasty: str = "",
    artifact_type: str = "",
    glaze_color: str = "",
    pageNum: int = 1,
    pageSize: int = 10,
):
    query = Artifacts.filter(name__contains=name)
    if dynasty:
        query = query.filter(era__contains=dynasty)
    if artifact_type:
        query = query.filter(type__contains=artifact_type)
    if glaze_color:
        query = query.filter(glaze__contains=glaze_color)

    artifact_list = await query.offset((pageNum - 1) * pageSize).limit(pageSize)
    artifact_list = [
        to_timeline_item(ArtifactsPydantic.model_validate(a).model_dump())
        for a in artifact_list
    ]
    total = await query.count()
    pageinfo = PageInfo(total=total, list=artifact_list)
    return Result.success(pageinfo)


