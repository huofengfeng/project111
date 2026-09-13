from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import create_model
from tortoise.contrib.pydantic import pydantic_model_creator

from common.exception_handler import CustomException
from common.result import Result, PageInfo
from models import Artifacts
from utils.auth import require_admin

router = APIRouter(prefix="/artifacts")

ArtifactsPydantic = pydantic_model_creator(Artifacts)

ArtifactsCreatePydantic = create_model(
    "ArtifactsPydantic",
    **{
        name: (Optional[field.annotation], None)
        for name, field in ArtifactsPydantic.model_fields.items()
    }
)


# 新增
@router.post("/add")
async def add(data: ArtifactsCreatePydantic, current_user=Depends(require_admin)):
    create_data = data.model_dump(exclude_unset=True, exclude={'id'})
    await Artifacts.create(**create_data)
    return Result.success()


# 修改
@router.put("/update")
async def update(data: ArtifactsCreatePydantic, current_user=Depends(require_admin)):
    update_data = data.model_dump(exclude_unset=True, exclude={"id"})
    await Artifacts.filter(id=data.id).update(**update_data)
    return Result.success()


# 删除
@router.delete("/delete/{artifact_id}")
async def delete(artifact_id: int, current_user=Depends(require_admin)):
    await Artifacts.filter(id=artifact_id).delete()
    return Result.success()


# 批量删除
@router.delete("/deleteBatch")
async def delete_batch(ids: List[int], current_user=Depends(require_admin)):
    await Artifacts.filter(id__in=ids).delete()
    return Result.success()


# 单个查询
@router.get("/selectById/{artifact_id}")
async def select_one(artifact_id: int):
    artifact = await Artifacts.get_or_none(id=artifact_id)
    if artifact is None:
        raise CustomException("文物不存在")
    return Result.success(ArtifactsPydantic.model_validate(artifact).model_dump())


# 查询所有
@router.get("/selectAll")
async def select_all(name: str = ""):
    artifact_list = await Artifacts.filter(name__contains=name)
    artifact_list = [
        ArtifactsPydantic.model_validate(a).model_dump()
        for a in artifact_list
    ]
    return Result.success(artifact_list)


# 分页查询
@router.get("/selectPage")
async def select_page(
    name: str = "",
    era: str = "",
    type: str = "",
    museum: str = "",
    pageNum: int = 1,
    pageSize: int = 10,
):
    query = Artifacts.filter(name__contains=name)
    if era:
        query = query.filter(era__contains=era)
    if type:
        query = query.filter(type__contains=type)
    if museum:
        query = query.filter(museum__contains=museum)

    artifact_list = await query.offset((pageNum - 1) * pageSize).limit(pageSize)
    artifact_list = [
        ArtifactsPydantic.model_validate(a).model_dump()
        for a in artifact_list
    ]
    total = await query.count()
    pageinfo = PageInfo(total=total, list=artifact_list)
    return Result.success(pageinfo)


# 筛选选项
@router.get("/filters")
async def get_filters():
    """返回年代、器型、馆藏地选项"""
    all_artifacts = await Artifacts.all().values("era", "type", "museum")

    eras = sorted(set(a["era"] for a in all_artifacts if a["era"]))
    types = sorted(set(a["type"] for a in all_artifacts if a["type"]))
    museums = sorted(set(a["museum"] for a in all_artifacts if a["museum"]))

    return Result.success({
        "eras": eras,
        "types": types,
        "museums": museums,
    })
