from typing import Optional
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from gargula.models.media import Media

class MediaRepository:
    @staticmethod
    async def find_by_id(session: AsyncSession, media_id: UUID) -> Optional[Media]:
        return await session.get(Media, media_id)

    @staticmethod
    async def create(session: AsyncSession, media: Media) -> Media:
        session.add(media)
        await session.commit()
        await session.refresh(media)
        return media

    @staticmethod
    async def delete(session: AsyncSession, media: Media) -> None:
        await session.delete(media)
        await session.commit()
