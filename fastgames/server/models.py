from typing import Any, Optional

from pydantic import BaseModel


class RequestModel(BaseModel):
    name: str
    data: Optional[dict[str, Any]] = {}


class ResponseModel(BaseModel):
    name: str
    data: Any
