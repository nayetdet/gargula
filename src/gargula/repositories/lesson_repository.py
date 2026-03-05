from typing import Optional, Set, cast
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col
from gargula.models.lesson import Lesson
from gargula.models.media import Media

class LessonRepository:
    __SORTABLE_COLUMNS: Set[str] = {
        "id",
        "name",
        "description",
        "subject_id",
        "created_at",
        "updated_at"
    }

    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
        name: Optional[str] = None,
        description: Optional[str] = None,
        subject_id: Optional[UUID] = None,
        embedding: Optional[list[float]] = None,
        page: int = 0,
        size: int = 10,
        sort_by: Optional[str] = None,
        sort_dir: str = "asc"
    ) -> list[Lesson]:
        stmt = select(Lesson)
        if name is not None:
            stmt = stmt.where(col(Lesson.name).ilike(f"%{name}%"))
        if description is not None:
            stmt = stmt.where(col(Lesson.description).ilike(f"%{description}%"))
        if subject_id is not None:
            stmt = stmt.where(col(Lesson.subject_id) == subject_id)
        if embedding is not None:
            stmt = (
                stmt
                .join(Media, col(Lesson.media_id) == col(Media.id))
                .where(col(Media.embedding).is_not(None))
                .order_by(col(Media.embedding).cosine_distance(embedding), col(Lesson.id))
            )
        else:
            sort_column = col(getattr(Lesson, sort_by)) if sort_by in cls.__SORTABLE_COLUMNS else col(Lesson.id)
            stmt = stmt.order_by(sort_column.desc() if sort_dir == "desc" else sort_column.asc())

        stmt = stmt.offset(page * size).limit(size)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def find_by_id(session: AsyncSession, lesson_id: UUID) -> Optional[Lesson]:
        return await session.get(Lesson, lesson_id)

    @staticmethod
    async def create(session: AsyncSession, lesson: Lesson) -> Lesson:
        session.add(lesson)
        await session.commit()
        await session.refresh(lesson)
        return lesson

    @staticmethod
    async def update(session: AsyncSession, lesson_id: UUID, lesson: Lesson) -> Optional[Lesson]:
        existing_lesson: Optional[Lesson] = await session.get(Lesson, lesson_id)
        if existing_lesson is None:
            return None

        existing_lesson.name = lesson.name
        existing_lesson.description = lesson.description
        existing_lesson.subject_id = lesson.subject_id

        await session.commit()
        await session.refresh(existing_lesson)
        return existing_lesson

    @staticmethod
    async def delete(session: AsyncSession, lesson: Lesson) -> None:
        await session.delete(lesson)
        await session.commit()

    @staticmethod
    async def count(
        session: AsyncSession,
        name: Optional[str] = None,
        description: Optional[str] = None,
        subject_id: Optional[UUID] = None,
        embedding: Optional[list[float]] = None
    ) -> int:
        stmt = select(func.count(Lesson.id))
        if name is not None:
            stmt = stmt.where(col(Lesson.name).ilike(f"%{name}%"))
        if description is not None:
            stmt = stmt.where(col(Lesson.description).ilike(f"%{description}%"))
        if subject_id is not None:
            stmt = stmt.where(col(Lesson.subject_id) == subject_id)
        if embedding is not None:
            stmt = stmt.join(Media, col(Lesson.media_id) == col(Media.id)).where(col(Media.embedding).is_not(None))
        result = await session.execute(stmt)
        return int(result.scalar_one())
