from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import create_model
from tortoise.contrib.pydantic import pydantic_model_creator

from common.exception_handler import CustomException
from common.result import Result, PageInfo
from models import User
from utils.auth import get_current_user, hash_password

router = APIRouter(prefix="/user", dependencies=[Depends(get_current_user)])
UserPydantic = pydantic_model_creator(User)
UserCreatePydantic = create_model(
    "UserPydantic",
    **{
        name: (Optional[field.annotation], None)
        for name, field in UserPydantic.model_fields.items()
    }
)


@router.post("/add")
async def add(user_create_pydantic: UserCreatePydantic):
    user = await User.get_or_none(username=user_create_pydantic.username)
    if user is not None:
        raise CustomException("账号重复")
    if user_create_pydantic.name is None:
        user_create_pydantic.name = user_create_pydantic.username
    if user_create_pydantic.password is None:
        user_create_pydantic.password = "123456"
    create_data = user_create_pydantic.model_dump(exclude_unset=True, exclude={'id'})
    create_data['role'] = 'User'
    create_data['password'] = hash_password(create_data['password'])
    await User.create(**create_data)
    return Result.success()


@router.put("/update")
async def update(user_create_pydantic: UserCreatePydantic):
    update_data = user_create_pydantic.model_dump(exclude_unset=True, exclude={"id"})
    if 'password' in update_data:
        update_data['password'] = hash_password(update_data['password'])
    await User.filter(id=user_create_pydantic.id).update(**update_data)
    return Result.success()


@router.delete("/delete/{user_id}")
async def delete(user_id: int):
    await User.filter(id=user_id).delete()
    return Result.success()


@router.delete("/deleteBatch")
async def delete_batch(ids: List[int]):
    await User.filter(id__in=ids).delete()
    return Result.success()


@router.get("/selectById/{user_id}")
async def select_one(user_id: int):
    user = await User.get_or_none(id=user_id)
    return Result.success(user)


@router.get("/selectAll")
async def select_all(name: str = ""):
    user_list = await User.filter(name__contains=name)
    return Result.success(user_list)


@router.get("/selectPage")
async def select_page(name: str = "", pageNum: int = 1, pageSize: int = 10):
    query = User.filter(name__contains=name)
    user_list = await query.offset((pageNum - 1) * pageSize).limit(pageSize)
    user_list = [
        UserPydantic.model_validate(user).model_dump()
        for user in user_list
    ]
    total = await query.count()
    pageinfo = PageInfo(total=total, list=user_list)
    return Result.success(pageinfo)
