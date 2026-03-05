import aioboto3
from typing import Optional
from aioboto3 import Session
from aiobotocore.client import AioBaseClient
from botocore.config import Config
from gargula.settings import settings

class S3Instance:
    __session: Optional[Session] = None

    @classmethod
    def get_session(cls) -> Session:
        if cls.__session is None:
            cls.__session = aioboto3.Session()
        return cls.__session

    @classmethod
    def get_client(cls) -> AioBaseClient:
        return cls.get_session().client(
            service_name="s3",
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key_id,
            aws_secret_access_key=settings.s3_secret_access_key,
            region_name=settings.s3_region,
            config=Config(
                s3={
                    "addressing_style": settings.s3_addressing_style
                }
            )
        )
