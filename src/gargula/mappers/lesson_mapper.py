from uuid import UUID
from gargula.mappers.media_mapper import MediaMapper
from gargula.mappers.subject_mapper import SubjectMapper
from gargula.models.lesson import Lesson
from gargula.schemas.requests.lesson_request_schema import LessonRequestSchema
from gargula.schemas.responses.lesson_response_schema import LessonResponseSchema

class LessonMapper:
    @staticmethod
    def to_model(request: LessonRequestSchema) -> Lesson:
        return Lesson(
            name=request.name,
            description=request.description,
            subject_id=request.subject_id,
        )

    @staticmethod
    def to_model_with_media(request: LessonRequestSchema, media_id: UUID) -> Lesson:
        return Lesson(
            name=request.name,
            description=request.description,
            subject_id=request.subject_id,
            media_id=media_id
        )

    @staticmethod
    def to_response_schema(lesson: Lesson) -> LessonResponseSchema:
        return LessonResponseSchema(
            id=lesson.id,
            name=lesson.name,
            description=lesson.description,
            subject=SubjectMapper.to_response_schema(lesson.subject),
            media=MediaMapper.to_response_schema(lesson.media)
        )
