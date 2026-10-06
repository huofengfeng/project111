from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from api import api_router
from common.exception_handler import setup_exceptions

from common.result import Result
from settings import TORTOISE_ORM

app = FastAPI()

# 跨域配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)


# 配置路由
app.include_router(api_router)
# 注册orm（启动时自动创建表）
register_tortoise(
    app,
    config=TORTOISE_ORM,
    add_exception_handlers=True,
    generate_schemas=True,
)
# 注册异常处理器
setup_exceptions(app)

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")
# 上传文件静态服务（供头像等图片直接展示）
app.mount("/uploads", StaticFiles(directory="files"), name="uploads")


@app.get("/")
async def root():
    return Result.success()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=9090)
