import pkgutil
import importlib
import re
from abc import ABC
from datetime import datetime, timezone
from typing import Set, Callable, ClassVar
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger
from starlette import status

class BaseApplicationException(ABC, Exception):
    STATUS_CODE: ClassVar[int]
    MESSAGE: ClassVar[str]
    INNER_EXCEPTION: ClassVar[type[Exception]]

    @classmethod
    def get_response(cls) -> JSONResponse:
        return JSONResponse(
            status_code=cls.STATUS_CODE,
            content={
                "status": cls.STATUS_CODE,
                "code": re.sub(r"([a-z])([A-Z])", r"\1_\2", cls.__name__).upper(),
                "message": cls.MESSAGE,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

class InternalServerErrorException(BaseApplicationException):
    STATUS_CODE: ClassVar[int] = status.HTTP_500_INTERNAL_SERVER_ERROR
    MESSAGE: ClassVar[str] = "An internal server error has occurred."
    INNER_EXCEPTION: ClassVar[type[Exception]] = Exception

def register_exception_handlers(app: FastAPI) -> None:
    def load_all_exceptions() -> None:
        for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
            importlib.import_module(f"{__name__}.{module_name}")

    def get_all_exceptions(cls = BaseApplicationException) -> Set[type[BaseApplicationException]]:
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_all_exceptions(subclass))
        return subclasses

    def exception_handler(exc_cls: type[BaseApplicationException]) -> Callable[[Request, Exception], JSONResponse]:
        def wrapper(_: Request, exc: Exception) -> JSONResponse:
            logger.exception(exc)
            return exc_cls.get_response()
        return wrapper

    load_all_exceptions()
    for exception_class in get_all_exceptions():
        inner_exception_class = getattr(exception_class, "INNER_EXCEPTION", None)
        app.add_exception_handler(inner_exception_class or exception_class, exception_handler(exception_class))
