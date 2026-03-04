from typing import Callable

from .handler import Handler


class Router:
    def __init__(self):
        self.handlers: dict[str, Handler] = {}

    def check_request(self, request_name: str):
        def decorator(function: Callable):
            self.handlers[request_name] = Handler(function=function)

        return decorator
