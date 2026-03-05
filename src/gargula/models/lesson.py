from typing import Optional
from uuid import UUID
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship
from gargula.models.base_model import BaseModel

class Lesson(BaseModel, table=True):
    __tablename__ = "lessons"

    name: str = Field(sa_column=Column(String(), nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column(String(length=2500), nullable=True))
    subject_id: UUID = Field(foreign_key="subjects.id")
    subject: "Subject" = Relationship(
        back_populates="lessons",
        sa_relationship_kwargs={
            "lazy": "selectin"
        }
    )

    media_id: Optional[UUID] = Field(nullable=False, unique=True, foreign_key="medias.id")
    media: Optional["Media"] = Relationship(
        back_populates="lesson",
        sa_relationship_kwargs={
            "uselist": False,
            "lazy": "selectin",
        }
    )
