from typing import Any

from pydantic import BaseModel


class RequestModel(BaseModel):
    name: str
    data: dict[str, Any]


class ResponseModel(BaseModel):
    name: str
    data: Any
