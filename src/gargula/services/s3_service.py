import os
import uuid
from typing import Optional, Set
from fastapi import UploadFile
from gargula.deps.s3_instance import S3Instance
from gargula.exceptions.s3_exceptions import S3UnsupportedContentTypeException

class S3Service:
    @staticmethod
    async def upload(bucket: str, file: UploadFile, allowed_extensions: Optional[Set[str]] = None) -> str:
        ext: str = os.path.splitext(file.filename)[1]
        key: str = f"{bucket}/{uuid.uuid4()}-{file.filename}{ext}"
        if allowed_extensions and ext not in allowed_extensions:
            raise S3UnsupportedContentTypeException()

        await file.seek(0)
        async with S3Instance.get_client() as s3:
            await s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=file.file,
                ContentType=file.content_type
            )

        return key

    @staticmethod
    async def delete(bucket: str, key: str) -> None:
        async with S3Instance.get_client() as s3:
            await s3.delete_object(
                Bucket=bucket,
                Key=key
            )
