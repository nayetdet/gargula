from typing import Optional, List
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String, Text
from sqlmodel import Field, Relationship
from gargula.models.base_model import BaseModel

class Media(BaseModel, table=True):
    __tablename__ = "medias"

    key: str = Field(sa_column=Column(String(), nullable=False))
    transcription: str = Field(sa_column=Column(Text(), nullable=False))
    embedding: Optional[List[float]] = Field(default=None, sa_column=Column(Vector(384)))
    lesson: Optional["Lesson"] = Relationship(
        back_populates="media",
        sa_relationship_kwargs={
            "uselist": False
        }
    )
