from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from gargula.deps.database_instance import DatabaseInstance
from gargula.schemas.queries.subject_query_schema import SubjectQuerySchema
from gargula.schemas.requests.subject_request_schema import SubjectRequestSchema
from gargula.services.subject_service import SubjectService

router = APIRouter()

@router.get("/")
async def find_all(query: SubjectQuerySchema = Depends(), session: AsyncSession = Depends(DatabaseInstance.get_session)):
    return await SubjectService.find_all(session, query)

@router.get("/{subject_id}")
async def find_by_id(subject_id: UUID, session: AsyncSession = Depends(DatabaseInstance.get_session)):
    return await SubjectService.find_by_id(session, subject_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(request: SubjectRequestSchema, session: AsyncSession = Depends(DatabaseInstance.get_session)):
    return await SubjectService.create(session, request)

@router.put("/{subject_id}")
async def update(subject_id: UUID, request: SubjectRequestSchema, session: AsyncSession = Depends(DatabaseInstance.get_session)):
    return await SubjectService.update(session, subject_id, request)

@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(subject_id: UUID, session: AsyncSession = Depends(DatabaseInstance.get_session)):
    await SubjectService.delete_by_id(session, subject_id)
