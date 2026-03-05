from typing import ClassVar
from starlette import status
from gargula.exceptions import BaseApplicationException

class S3UnsupportedContentTypeException(BaseApplicationException):
    STATUS_CODE: ClassVar[int] = status.HTTP_400_BAD_REQUEST
    MESSAGE: ClassVar[str] = "Unsupported content type for uploaded file."
