from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import create_model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.functions import Count

from common.exception_handler import CustomException
from common.result import Result, PageInfo
from models import Tombs, Artifacts
from utils.auth import require_admin

router = APIRouter(prefix="/tombs")

TombsPydantic = pydantic_model_creator(Tombs)

TombsCreatePydantic = create_model(
    "TombsCreatePydantic",
    **{
        name: (Optional[field.annotation], None)
        for name, field in TombsPydantic.model_fields.items()
    }
)


# ====== 基础 CRUD ======

@router.post("/add")
async def add(data: TombsCreatePydantic, current_user=Depends(require_admin)):
    create_data = data.model_dump(exclude_unset=True, exclude={'id'})
    await Tombs.create(**create_data)
    return Result.success()


@router.put("/update")
async def update(data: TombsCreatePydantic, current_user=Depends(require_admin)):
    update_data = data.model_dump(exclude_unset=True, exclude={"id"})
    await Tombs.filter(id=data.id).update(**update_data)
    return Result.success()


@router.delete("/delete/{tomb_id}")
async def delete(tomb_id: int, current_user=Depends(require_admin)):
    await Tombs.filter(id=tomb_id).delete()
    return Result.success()


@router.delete("/deleteBatch")
async def delete_batch(ids: List[int], current_user=Depends(require_admin)):
    await Tombs.filter(id__in=ids).delete()
    return Result.success()


@router.get("/selectById/{tomb_id}")
async def select_one(tomb_id: int):
    tomb = await Tombs.get_or_none(id=tomb_id)
    return Result.success(tomb)


@router.get("/selectAll")
async def select_all(name: str = ""):
    tomb_list = await Tombs.filter(name__contains=name)
    return Result.success(tomb_list)


@router.get("/selectPage")
async def select_page(
    name: str = "",
    location: str = "",
    era: str = "",
    pageNum: int = 1,
    pageSize: int = 10,
):
    query = Tombs.filter(name__contains=name)
    if location:
        query = query.filter(location__contains=location)
    if era:
        query = query.filter(era__contains=era)

    tomb_list = await query.offset((pageNum - 1) * pageSize).limit(pageSize)
    tomb_list = [
        TombsPydantic.model_validate(t).model_dump()
        for t in tomb_list
    ]
    total = await query.count()
    pageinfo = PageInfo(total=total, list=tomb_list)
    return Result.success(pageinfo)


# ====== 出土可视化专用接口 ======

# 出土地点分布数据
@router.get("/map/locations")
async def get_map_locations():
    """返回所有墓葬的出土地点及经纬度，用于地图可视化"""
    data = await Tombs.filter(longitude__isnull=False, latitude__isnull=False).values(
        "id", "name", "location", "era", "longitude", "latitude", "sancai_items", "total_items"
    )
    return Result.success(data)


# 按出土地点查询关联文物
@router.get("/map/artifacts")
async def get_map_artifacts(location: str = ""):
    """根据出土地点查询关联的文物信息，用于地图联动"""
    if not location:
        return Result.success([])
    # 从 location 中提取核心地名（如"洛阳龙门东山北麓"→"洛阳"）
    keywords = []
    for kw in ["洛阳", "西安", "乾县", "巩义", "郑州", "礼泉", "凤翔", "太原", "扬州", "咸阳", "偃师", "孟津", "新安"]:
        if kw in location:
            keywords.append(kw)
    if not keywords:
        # 没有匹配到关键词，用完整 location 模糊搜索
        data = await Artifacts.filter(source__contains=location).values(
            "id", "name", "era", "type", "size", "glaze", "source", "museum", "level", "image_url"
        )
        return Result.success(data)
    # 用关键词搜索，取并集
    result = {}
    for kw in keywords:
        rows = await Artifacts.filter(source__contains=kw).values(
            "id", "name", "era", "type", "size", "glaze", "source", "museum", "level", "image_url"
        )
        for row in rows:
            result[row["id"]] = row
    return Result.success(list(result.values()))


# 筛选选项
@router.get("/meta/filters")
async def get_filter_options():
    """返回供筛选下拉框使用的唯一值列表"""
    locations = await Tombs.all().distinct().values_list("location", flat=True)
    eras = await Tombs.all().distinct().values_list("era", flat=True)
    return Result.success({
        "locations": [loc for loc in locations if loc],
        "eras": [e for e in eras if e],
    })


# 统计概览
@router.get("/stats/overview")
async def get_stats_overview():
    """返回统计概览：墓葬总数、按地区分布、按年代分布"""
    total = await Tombs.all().count()

    # 按地区统计
    location_stats = await Tombs.all().group_by("location").annotate(count=Count("id")).values("location", "count")
    location_distribution = [{"name": loc["location"], "count": loc["count"]} for loc in location_stats if loc["location"]]

    # 按年代统计
    era_stats = await Tombs.all().group_by("era").annotate(count=Count("id")).values("era", "count")
    era_distribution = [{"name": e["era"], "count": e["count"]} for e in era_stats if e["era"]]

    return Result.success({
        "total": total,
        "location_distribution": location_distribution,
        "era_distribution": era_distribution,
    })


# 交叉维度统计
@router.get("/stats/cross")
async def get_cross_stats():
    """按地区×年代交叉统计，用于热力图/堆叠图"""
    stats = await (
        Tombs.all()
        .group_by("location", "era")
        .annotate(count=Count("id"))
        .values("location", "era", "count")
    )
    data = [
        {"location": s["location"], "era": s["era"], "count": s["count"]}
        for s in stats if s["location"] and s["era"]
    ]
    return Result.success(data)
