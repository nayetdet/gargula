from typing import ClassVar
from starlette import status
from gargula.exceptions import BaseApplicationException

class MediaNotFoundException(BaseApplicationException):
    STATUS_CODE: ClassVar[int] = status.HTTP_404_NOT_FOUND
    MESSAGE: ClassVar[str] = "The requested media was not found."
