from typing import Optional
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from gargula.models.subject import Subject

class SubjectRepository:
    @staticmethod
    async def find_by_id(session: AsyncSession, subject_id: UUID) -> Optional[Subject]:
        return await session.get(Subject, subject_id)

    @staticmethod
    async def create(session: AsyncSession, subject: Subject) -> Subject:
        session.add(subject)
        await session.commit()
        await session.refresh(subject)
        return subject

    @staticmethod
    async def update(session: AsyncSession, subject_id: UUID, subject: Subject) -> Optional[Subject]:
        existing_subject: Optional[Subject] = await session.get(Subject, subject_id)
        if existing_subject is None:
            return None

        existing_subject.name = subject.name
        existing_subject.semester = subject.semester
        existing_subject.professor = subject.professor

        await session.commit()
        await session.refresh(existing_subject)
        return existing_subject

    @staticmethod
    async def delete(session: AsyncSession, subject: Subject) -> None:
        await session.delete(subject)
        await session.commit()
