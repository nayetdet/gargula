from typing import Optional
from uuid import UUID
from gargula.schemas.queries.base_query_schema import BaseQuerySchema

class LessonQuerySchema(BaseQuerySchema):
    name: Optional[str] = None
    description: Optional[str] = None
    media_transcription: Optional[str] = None
    subject_id: Optional[UUID] = None
