from typing import Callable

from .handler import Handler


class Router:
    def __init__(self):
        self.handlers: dict[str, Handler] = {}

    def check_request(self, name: str):
        def decorator(function: Callable):
            self.handlers[name] = Handler(function=function)

        return decorator
