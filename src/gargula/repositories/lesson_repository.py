from typing import Optional
from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from gargula.models.lesson import Lesson

class LessonRepository:
    @staticmethod
    async def find_by_id(session: AsyncSession, lesson_id: UUID) -> Optional[Lesson]:
        result = await session.exec(select(Lesson).where(Lesson.id == lesson_id))
        return result.first()

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
