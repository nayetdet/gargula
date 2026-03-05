from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from gargula.schemas.responses.media_response_schema import MediaResponseSchema
from gargula.schemas.responses.subject_response_schema import SubjectResponseSchema

class LessonResponseSchema(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    subject: SubjectResponseSchema
    media: MediaResponseSchema
