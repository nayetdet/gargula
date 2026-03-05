from typing import Optional
from uuid import UUID
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from gargula.exceptions.lesson_exceptions import LessonNotFoundException
from gargula.mappers.lesson_mapper import LessonMapper
from gargula.models.lesson import Lesson
from gargula.repositories.lesson_repository import LessonRepository
from gargula.schemas.requests.lesson_request_schema import LessonRequestSchema
from gargula.schemas.responses.media_response_schema import MediaResponseSchema
from gargula.schemas.responses.lesson_response_schema import LessonResponseSchema
from gargula.services.media_service import MediaService

class LessonService:
    @staticmethod
    async def find_by_id(session: AsyncSession, lesson_id: UUID) -> LessonResponseSchema:
        lesson: Optional[Lesson] = await LessonRepository.find_by_id(session, lesson_id)
        if lesson is None:
            raise LessonNotFoundException()
        return LessonMapper.to_response_schema(lesson)

    @staticmethod
    async def create(session: AsyncSession, request: LessonRequestSchema, media_file: UploadFile) -> LessonResponseSchema:
        media_response: MediaResponseSchema = await MediaService.create(session, media_file)
        try:
            lesson: Lesson = await LessonRepository.create(session, LessonMapper.to_model_with_media(request, media_response.id))
            return LessonMapper.to_response_schema(lesson)
        except Exception:
            await MediaService.delete_by_id(session, media_response.id)
            raise

    @staticmethod
    async def update(session: AsyncSession, lesson_id: UUID, request: LessonRequestSchema) -> LessonResponseSchema:
        lesson: Optional[Lesson] = await LessonRepository.update(session, lesson_id, LessonMapper.to_model(request))
        if lesson is None:
            raise LessonNotFoundException()
        return LessonMapper.to_response_schema(lesson)

    @staticmethod
    async def delete(session: AsyncSession, lesson_id: UUID) -> None:
        lesson: Optional[Lesson] = await LessonRepository.find_by_id(session, lesson_id)
        if lesson is None:
            raise LessonNotFoundException()
        await LessonRepository.delete(session, lesson)
        await MediaService.delete_by_id(session, lesson.media_id)
