from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from gargula.exceptions.subject_exceptions import SubjectNotFoundException
from gargula.mappers.subject_mapper import SubjectMapper
from gargula.models.subject import Subject
from gargula.repositories.subject_repository import SubjectRepository
from gargula.schemas.queries.base_query_schema import PageSchema, PageableSchema
from gargula.schemas.queries.subject_query_schema import SubjectQuerySchema
from gargula.schemas.requests.subject_request_schema import SubjectRequestSchema
from gargula.schemas.responses.subject_response_schema import SubjectResponseSchema

class SubjectService:
    @staticmethod
    async def find_all(session: AsyncSession, query: SubjectQuerySchema) -> PageSchema[SubjectResponseSchema]:
        return PageSchema[SubjectResponseSchema](
            content=[
                SubjectMapper.to_response_schema(subject)
                for subject in await SubjectRepository.find_all(
                    session=session,
                    name=query.name,
                    semester=query.semester,
                    professor=query.professor,
                    page=query.page,
                    size=query.size,
                    sort_by=query.sort_by,
                    sort_dir=query.sort_dir,
                )
            ],
            pageable=PageableSchema(
                page=query.page,
                size=query.size,
                total_elements=await SubjectRepository.count(
                    session=session,
                    name=query.name,
                    semester=query.semester,
                    professor=query.professor,
                )
            )
        )

    @staticmethod
    async def find_by_id(session: AsyncSession, subject_id: UUID) -> SubjectResponseSchema:
        subject: Optional[Subject] = await SubjectRepository.find_by_id(session, subject_id)
        if subject is None:
            raise SubjectNotFoundException()
        return SubjectMapper.to_response_schema(subject)

    @staticmethod
    async def create(session: AsyncSession, request: SubjectRequestSchema) -> SubjectResponseSchema:
        subject: Subject = await SubjectRepository.create(session, SubjectMapper.to_model(request))
        return SubjectMapper.to_response_schema(subject)

    @staticmethod
    async def update(session: AsyncSession, subject_id: UUID, request: SubjectRequestSchema) -> SubjectResponseSchema:
        subject: Optional[Subject] = await SubjectRepository.update(session, subject_id, SubjectMapper.to_model(request))
        if subject is None:
            raise SubjectNotFoundException()
        return SubjectMapper.to_response_schema(subject)

    @staticmethod
    async def delete_by_id(session: AsyncSession, subject_id: UUID) -> None:
        subject: Optional[Subject] = await SubjectRepository.find_by_id(session, subject_id)
        if subject is None:
            raise SubjectNotFoundException()
        await SubjectRepository.delete(session, subject)
