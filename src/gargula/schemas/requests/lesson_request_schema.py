from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class LessonRequestSchema(BaseModel):
    name: str = Field(min_length=1)
    description: Optional[str] = Field(default=None, max_length=2500)
    subject_id: UUID
