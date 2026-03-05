from typing import Optional, List
from sqlalchemy import Column
from pgvector.sqlalchemy import Vector
from sqlmodel import Field
from gargula.models.base_model import BaseModel

class Media(BaseModel, table=True):
    __tablename__ = "medias"

    key: str = Field(nullable=False)
    transcription: str = Field(sa_column=Column(nullable=False))
    embedding: Optional[List[float]] = Field(default=None, sa_column=Column(Vector(384)))
