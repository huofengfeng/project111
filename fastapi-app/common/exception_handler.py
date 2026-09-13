from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse


class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message


class UnauthorizedError(CustomException):
    def __init__(self, message: str = "未登录或登录已过期"):
        super().__init__(message)


def setup_exceptions(app: FastAPI):
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        status_code = status.HTTP_401_UNAUTHORIZED if isinstance(exc, UnauthorizedError) else status.HTTP_200_OK
        return JSONResponse(
            status_code=status_code,
            content={"code": "401" if isinstance(exc, UnauthorizedError) else "500", "msg": exc.message}
        )

    @app.exception_handler(RequestValidationError)
    async def validate_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"code": "500", "msg": "请求参数错误"}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"code": "500", "msg": "系统错误"}
        )
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response
