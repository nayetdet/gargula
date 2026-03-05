from typing import List
from sqlmodel import Relationship, Field
from gargula.models.base_model import BaseModel

class Subject(BaseModel, table=True):
    __tablename__ = "subjects"

    name: str = Field(nullable=False)
    semester: str = Field(nullable=False)
    professor: str = Field(nullable=False)
    lessons: List["Lesson"] = Relationship(
        back_populates="subject",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan"
        }
    )
