import aioboto3
from typing import Optional
from aioboto3 import Session
from aiobotocore.client import AioBaseClient

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
            endpoint_url="http://localhost:3900",
            aws_access_key_id="GK123",
            aws_secret_access_key="SK456"
        )
