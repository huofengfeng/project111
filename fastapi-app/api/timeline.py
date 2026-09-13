from fastapi import APIRouter
from tortoise.contrib.pydantic import pydantic_model_creator

from common.result import Result
from models import Artifacts
from api.artifact import to_timeline_item

router = APIRouter(prefix="/timeline")

# 时期定义与映射
PERIOD_CONFIG = [
    {
        "name": "初唐",
        "year": "618-712",
        "description": "唐三彩开始出现，造型相对简单，釉色以黄、绿为主。",
        "event": "唐朝建立",
        "keywords": ["初唐", "贞观"],
    },
    {
        "name": "盛唐",
        "year": "713-766",
        "description": "唐三彩鼎盛期，造型丰富多样，釉色鲜艳，人物俑和动物俑大量出现。",
        "event": "开元盛世",
        "keywords": ["盛唐", "开元", "天宝"],
    },
    {
        "name": "中唐",
        "year": "766-835",
        "description": "风格趋于写实，器型更加规整，部分出现绞胎工艺。",
        "event": "安史之乱后",
        "keywords": ["中唐"],
    },
    {
        "name": "晚唐",
        "year": "836-907",
        "description": "唐三彩逐渐衰落，产量减少，风格趋于简化。",
        "event": "藩镇割据",
        "keywords": ["晚唐"],
    },
]


def _match_period(era: str) -> str:
    """根据 era 字段值匹配时期名称"""
    if not era:
        return "其他"
    for period in PERIOD_CONFIG:
        for kw in period["keywords"]:
            if kw in era:
                return period["name"]
    return "其他"


ArtifactsPydantic = pydantic_model_creator(Artifacts)


@router.get("/periods")
async def get_timeline_data():
    """返回按时期分组的文物列表，用于时间线可视化"""
    all_artifacts = await Artifacts.all()

    # 按时期分组
    grouped = {}
    for period in PERIOD_CONFIG:
        grouped[period["name"]] = []

    for art in all_artifacts:
        period_name = _match_period(art.era or "")
        if period_name in grouped:
            grouped[period_name].append(art)
        else:
            grouped.setdefault("其他", []).append(art)

    # 构建返回数据
    result = []
    for period in PERIOD_CONFIG:
        items = grouped.get(period["name"], [])
        artifact_data = [
            to_timeline_item(ArtifactsPydantic.model_validate(a).model_dump())
            for a in items
        ]
        result.append({
            "name": period["name"],
            "year": period["year"],
            "description": period["description"],
            "event": period["event"],
            "count": len(artifact_data),
            "artifacts": artifact_data,
        })

    return Result.success(result)


@router.get("/{period_name}")
async def get_period_artifacts(period_name: str):
    """返回指定时期的文物列表"""
    artifacts = await Artifacts.all()
    matched = [a for a in artifacts if _match_period(a.era or "") == period_name]
    artifact_data = [
        to_timeline_item(ArtifactsPydantic.model_validate(a).model_dump())
        for a in matched
    ]
    # 查找时期配置
    config = next((p for p in PERIOD_CONFIG if p["name"] == period_name), None)
    return Result.success({
        "name": period_name,
        "description": config["description"] if config else "",
        "event": config["event"] if config else "",
        "count": len(artifact_data),
        "artifacts": artifact_data,
    })
