from typing import Optional, Set
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col
from gargula.models.subject import Subject

class SubjectRepository:
    __SORTABLE_COLUMNS: Set[str] = {
        "id",
        "name",
        "semester",
        "professor",
        "created_at",
        "updated_at"
    }

    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
        name: Optional[str] = None,
        semester: Optional[str] = None,
        professor: Optional[str] = None,
        page: int = 0,
        size: int = 10,
        sort_by: Optional[str] = None,
        sort_dir: str = "asc"
    ) -> list[Subject]:
        stmt = select(Subject)
        if name is not None:
            stmt = stmt.where(col(Subject.name).ilike(f"%{name}%"))
        if semester is not None:
            stmt = stmt.where(col(Subject.semester).ilike(f"%{semester}%"))
        if professor is not None:
            stmt = stmt.where(col(Subject.professor).ilike(f"%{professor}%"))

        sort_column = getattr(Subject, sort_by) if sort_by in cls.__SORTABLE_COLUMNS else Subject.id
        stmt = stmt.order_by(sort_column.desc() if sort_dir == "desc" else sort_column.asc())
        stmt = stmt.offset(page * size).limit(size)
        result = await session.execute(stmt)
        return list(result.scalars().all())

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

    @staticmethod
    async def count(
        session: AsyncSession,
        name: Optional[str] = None,
        semester: Optional[str] = None,
        professor: Optional[str] = None
    ) -> int:
        stmt = select(func.count(Subject.id))
        if name is not None:
            stmt = stmt.where(col(Subject.name).ilike(f"%{name}%"))
        if semester is not None:
            stmt = stmt.where(col(Subject.semester).ilike(f"%{semester}%"))
        if professor is not None:
            stmt = stmt.where(col(Subject.professor).ilike(f"%{professor}%"))
        result = await session.execute(stmt)
        return int(result.scalar_one())
