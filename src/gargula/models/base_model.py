from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field

class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now, sa_column=Column(DateTime, nullable=False))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, sa_column=Column(DateTime, nullable=False, onupdate=datetime.now))
