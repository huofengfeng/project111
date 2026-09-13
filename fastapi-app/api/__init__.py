import importlib
import pkgutil

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from common.exception_handler import CustomException, UnauthorizedError
from common.result import Result
from models import Admin, User
from utils.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)


class Account(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    username: str | None = None
    password: str | None = None
    newPassword: str | None = None
    role: str | None = None
    name: str | None = None
    avatar: str | None = None


api_router = APIRouter()


@api_router.post("/login")
async def login(account: Account):
    # 根据前端选择的 role 只查对应表
    if account.role == 'Admin':
        admin = await Admin.get_or_none(username=account.username)
        if admin is None:
            raise UnauthorizedError("账号或密码错误")
        if not verify_password(account.password, admin.password):
            raise UnauthorizedError("账号或密码错误")
        # 明文密码自动升级为 bcrypt 哈希
        if not admin.password.startswith("$2b$"):
            await Admin.filter(id=admin.id).update(password=hash_password(admin.password))
        token = create_access_token(data={"sub": str(admin.id), "role": admin.role})
        user_data = Account.model_validate(admin)
        return Result.success({
            "access_token": token,
            "token_type": "bearer",
            "user": user_data,
        })
    else:
        import traceback
        try:
            user = await User.get_or_none(username=account.username)
            if user is None:
                raise UnauthorizedError("账号或密码错误")
            if not verify_password(account.password, user.password):
                raise UnauthorizedError("账号或密码错误")
            token = create_access_token(data={"sub": str(user.id), "role": user.role})
            user_data = Account.model_validate(user)
            return Result.success({
                "access_token": token,
                "token_type": "bearer",
                "user": user_data,
            })
        except CustomException:
            raise
        except Exception as e:
            traceback.print_exc()
            raise CustomException(f"用户登录异常: {str(e)}")


@api_router.put("/updatePassword")
async def update_password(account: Account, current_user=Depends(get_current_user)):
    if not verify_password(account.password, current_user.password):
        raise CustomException("原密码错误")
    if account.password == account.newPassword:
        raise CustomException("新密码不能与原密码相同")
    if isinstance(current_user, Admin):
        await Admin.filter(id=current_user.id).update(password=hash_password(account.newPassword))
    else:
        await User.filter(id=current_user.id).update(password=hash_password(account.newPassword))
    return Result.success()


class RegisterData(BaseModel):
    username: str
    password: str
    name: str | None = None


@api_router.post("/register")
async def register(data: RegisterData):
    import traceback
    try:
        existing = await User.get_or_none(username=data.username)
        if existing is not None:
            raise CustomException("账号重复")
        if data.name is None:
            data.name = data.username
        await User.create(
            username=data.username,
            password=hash_password(data.password),
            name=data.name,
            role='User',
        )
        return Result.success()
    except CustomException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise CustomException(f"注册异常: {str(e)}")


# 自动导入当前目录下的所有模块
for _, module_name, _ in pkgutil.iter_modules(__path__, __name__ + "."):
    module = importlib.import_module(module_name)
    if hasattr(module, "router"):
        # 假设每个端点文件都有一个 router 变量
        api_router.include_router(module.router)
