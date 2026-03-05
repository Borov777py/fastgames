from typing import Any, Optional

from pydantic import BaseModel

from .models import RequestModel, ResponseModel
from .handler import Handler
from .middleware import BaseMiddleware
from .router import Router


class Dispatcher:
    def __init__(
            self,
            handlers: Optional[dict[str, Handler]] = None,
            middlewares: Optional[list[BaseMiddleware]] = None
    ):
        self.__handlers: dict[str, Handler] = handlers or {}
        self.__middlewares: list[BaseMiddleware] = middlewares or []

    def include_routers(self, *args: Router) -> None:
        """Добавляет handlers из Routers в Dispatcher"""
        for router in args:
            self.__handlers.update(router.handlers)

    def register_middlewares(self, *args: BaseMiddleware) -> None:
        """Добавляет middlewares в Dispatcher"""
        for middleware in args:
            self.__middlewares.append(middleware)

    def handle_data(self, data: Any) -> dict[str, Any]:
        """Обработка полученных данных от клиента"""
        response: dict[str, Any] = {}

        for request in [RequestModel(**item) for item in data]:
            if (handler := self.__handlers.get(request.name, None)) is None:
                continue

            data: dict[str, Any] = {}

            data.update(
                {
                    name: parameter.annotation(**request.data)
                    for name, parameter in handler.parameters.items()
                    if issubclass(parameter.annotation, BaseModel)
                }
            )

            for middleware in self.__middlewares:
                middleware(handler=handler, data=data)

            result = handler(data=data)

            isinstance(result, ResponseModel) and response.update({result.name: result.data})

        return response
