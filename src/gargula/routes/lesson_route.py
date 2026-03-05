from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, File
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from gargula.deps.database_instance import DatabaseInstance
from gargula.schemas.requests.lesson_request_schema import LessonRequestSchema
from gargula.services.lesson_service import LessonService

router = APIRouter()

@router.get("/{lesson_id}")
async def find_by_id(lesson_id: UUID, session: AsyncSession = Depends(DatabaseInstance.get_session)):
    return await LessonService.find_by_id(session, lesson_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    request: LessonRequestSchema = Depends(LessonRequestSchema.as_form),
    media_file: UploadFile = File(...),
    session: AsyncSession = Depends(DatabaseInstance.get_session),
):
    return await LessonService.create(session, request, media_file)

@router.put("/{lesson_id}")
async def update(lesson_id: UUID, request: LessonRequestSchema, session: AsyncSession = Depends(DatabaseInstance.get_session)):
    return await LessonService.update(session, lesson_id, request)

@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(lesson_id: UUID, session: AsyncSession = Depends(DatabaseInstance.get_session)):
    await LessonService.delete(session, lesson_id)
