from pydantic import BaseModel
from fastapi import status


class BaseException(Exception):
    status_code: int
    message: str


class ExceptionResponse(BaseModel):
    status_code: int
    message: str


class PropertyNotFoundError(BaseException):
    def __init__(self, property_id: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = f"Property with id '{property_id}' not found"
