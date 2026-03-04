from abc import ABC, abstractmethod
from typing import Any

from .handler import Handler


class BaseMiddleware(ABC):
    @abstractmethod
    def __call__(self, handler: Handler, data: dict[str, Any]):
        pass
