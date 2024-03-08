from fastapi import status
from fastapi.responses import JSONResponse, Response
from typing import Union


class CommonResponse:
    @staticmethod
    def success(data: Union[dict, list, str] = None, message: str = "success") -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": message,
                "data": data
            }
        )

    @staticmethod
    def error(code: int, message: str) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": code,
                "message": message,
                "data": None
            }
        )

    @staticmethod
    def custom(status_code: int, code: int, message: str, data: Union[dict, list, str] = None) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "code": code,
                "message": message,
                "data": data
            }
        )

    @staticmethod
    def response(status_code: int, code: int, message: str, data: Union[dict, list, str] = None) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "code": code,
                "message": message,
                "data": data
            }
        )
