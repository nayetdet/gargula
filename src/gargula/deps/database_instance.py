from typing import Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker

class DatabaseInstance:
    __engine: Optional[AsyncEngine] = None
    __session: Optional[async_sessionmaker[AsyncSession]] = None

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        if cls.__engine is None:
            cls.__engine = create_async_engine(
                url="postgresql+asyncpg://user:password@localhost:5432/gargula",
                echo=True,
                pool_size=10,
                max_overflow=20,
            )
        return cls.__engine

    @classmethod
    def get_sessionmaker(cls) -> async_sessionmaker[AsyncSession]:
        if cls.__session is None:
            cls.__session = async_sessionmaker(
                cls.get_engine(),
                expire_on_commit=False,
            )
        return cls.__session

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        async with cls.get_sessionmaker()() as session:
            yield session
