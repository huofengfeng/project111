import random
from fastapi import APIRouter
from pydantic import BaseModel
from tortoise.functions import Count

from common.result import Result
from models import Artifacts

router = APIRouter(prefix="/quiz")


class GuessInput(BaseModel):
    artifact_id: int
    answer: str
    revealed_hints: int = 0


@router.get("/round")
async def get_round():
    """随机返回5道猜谜题，包含渐进式提示（不含答案）"""
    total = await Artifacts.annotate(count=Count("id")).values("count")
    count = total[0]["count"] if total else 0
    if count < 5:
        return Result.error("文物数据不足，至少需要5件文物")

    all_ids = await Artifacts.all().values_list("id", flat=True)
    selected_ids = random.sample(all_ids, 5)
    artifacts = await Artifacts.filter(id__in=selected_ids).all()

    questions = []
    for artifact in artifacts:
        hints = [
            {"label": "年代与釉色", "text": f"这件文物出自 {artifact.era or '未知'}，釉色为 {artifact.glaze or '暂无记载'}"},
            {"label": "器型与尺寸", "text": f"器型属于 {artifact.type or '未知'}，尺寸约 {artifact.size or '暂无记载'}"},
            {"label": "馆藏与来源", "text": f"现藏于 {artifact.museum or '未知'}，出土自 {artifact.source or '暂无记载'}"},
            {"label": "文物图片", "text": "请看下方图片辨认", "image": artifact.image_url or ""},
        ]
        questions.append({
            "id": artifact.id,
            "hints": hints,
            "level": artifact.level or "未定级",
        })

    return Result.success({"questions": questions})


@router.post("/guess")
async def check_guess(data: GuessInput):
    """校验用户猜测，根据已揭示提示数计分"""
    artifact = await Artifacts.get_or_none(id=data.artifact_id)
    if artifact is None:
        return Result.error("文物不存在")

    score_map = {0: 100, 1: 75, 2: 50, 3: 25}
    score = score_map.get(data.revealed_hints, 25)

    if data.answer.strip() == artifact.name.strip():
        return Result.success({
            "correct": True,
            "score": score,
            "name": artifact.name,
            "era": artifact.era,
            "type": artifact.type,
            "image_url": artifact.image_url,
        })
    else:
        return Result.success({
            "correct": False,
            "score": 0,
            "name": artifact.name,
        })