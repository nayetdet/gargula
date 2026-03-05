from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import DateTime
from sqlmodel import SQLModel, Field

class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_type=DateTime,
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_type=DateTime,
        nullable=False,
        sa_column_kwargs={
            "onupdate": datetime.now,
        }
    )
