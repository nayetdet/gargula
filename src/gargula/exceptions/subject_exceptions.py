from typing import ClassVar
from starlette import status
from gargula.exceptions import BaseApplicationException

class SubjectNotFoundException(BaseApplicationException):
    STATUS_CODE: ClassVar[int] = status.HTTP_404_NOT_FOUND
    MESSAGE: ClassVar[str] = "The requested subject was not found."
