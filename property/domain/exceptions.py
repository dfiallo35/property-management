from fastapi import status


class BaseException(Exception):
    status_code: int
    message: str


class PropertyNotFoundError(BaseException):
    def __init__(self, property_id: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = f"Property with id '{property_id}' not found"


class ConfigurationNotValidError(BaseException):
    def __init__(self, key: str, type: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = f"Configuration with key '{key}' and type '{type}' is not valid"
