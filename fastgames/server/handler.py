from typing import Callable, Any, Optional
from inspect import signature

from .models import ResponseModel


class Handler:
    def __init__(self, function: Callable):
        self.__function = function
        self.__signature = signature(self.__function)

        self.parameters = self.__signature.parameters

    def __call__(self, data: dict[str, Any]) -> Optional[ResponseModel]:
        return self.__function(
            **{
                name: parameter
                for name, parameter in data.items()
                if self.parameters.get(name, None) is not None
            }
        )
