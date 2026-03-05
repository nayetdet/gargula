from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from fastapi import Form

class LessonRequestSchema(BaseModel):
    name: str = Field(min_length=1)
    description: Optional[str] = Field(default=None, max_length=2500)
    subject_id: UUID

    @classmethod
    def as_form(
        cls,
        name: str = Form(..., min_length=1),
        description: Optional[str] = Form(default=None, max_length=2500),
        subject_id: UUID = Form(...),
    ) -> "LessonRequestSchema":
        return cls(name=name, description=description, subject_id=subject_id)
