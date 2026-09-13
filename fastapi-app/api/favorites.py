from fastapi import APIRouter, Depends
from pydantic import BaseModel

from common.result import Result
from models import Artifacts, Favorites
from utils.auth import get_current_user

router = APIRouter(prefix="/favorites")


class ToggleRequest(BaseModel):
    artifact_id: int


@router.post("/toggle")
async def toggle_favorite(data: ToggleRequest, current_user=Depends(get_current_user)):
    user_id = current_user.id
    existing = await Favorites.get_or_none(user_id=user_id, artifact_id=data.artifact_id)
    if existing:
        await existing.delete()
        return Result.success({"favorited": False})
    else:
        await Favorites.create(user_id=user_id, artifact_id=data.artifact_id)
        return Result.success({"favorited": True})


@router.get("/list")
async def list_favorites(current_user=Depends(get_current_user)):
    user_id = current_user.id
    favs = await Favorites.filter(user_id=user_id).values("artifact_id")
    ids = [f["artifact_id"] for f in favs]
    return Result.success(ids)


@router.get("/items")
async def list_favorite_items(current_user=Depends(get_current_user)):
    user_id = current_user.id
    favs = await Favorites.filter(user_id=user_id).values("artifact_id")
    artifact_ids = [f["artifact_id"] for f in favs]
    if not artifact_ids:
        return Result.success([])
    artifacts = await Artifacts.filter(id__in=artifact_ids)
    from tortoise.contrib.pydantic import pydantic_model_creator
    ArtifactsPydantic = pydantic_model_creator(Artifacts)
    items = [ArtifactsPydantic.model_validate(a).model_dump() for a in artifacts]
    return Result.success(items)