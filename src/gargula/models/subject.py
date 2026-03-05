from typing import List
from sqlalchemy import Column, String
from sqlmodel import Relationship, Field
from gargula.models.base_model import BaseModel

class Subject(BaseModel, table=True):
    __tablename__ = "subjects"

    name: str = Field(sa_column=Column(String(), nullable=False))
    semester: str = Field(sa_column=Column(String(), nullable=False))
    professor: str = Field(sa_column=Column(String(), nullable=False))
    lessons: List["Lesson"] = Relationship(
        back_populates="subject",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan"
        }
    )
