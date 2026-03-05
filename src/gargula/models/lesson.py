from typing import Optional
from uuid import UUID
from sqlmodel import Field, Relationship
from gargula.models.base_model import BaseModel

class Lesson(BaseModel, table=True):
    __tablename__ = "lessons"

    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None, max_length=2500)
    subject_id: UUID = Field(foreign_key="subjects.id")
    subject: "Subject" = Relationship(back_populates="lessons")
    media_id: Optional[UUID] = Field(nullable=False, unique=True, foreign_key="medias.id")
    media: Optional["Media"] = Relationship(
        back_populates="lesson",
        sa_relationship_kwargs={
            "uselist": False
        }
    )

