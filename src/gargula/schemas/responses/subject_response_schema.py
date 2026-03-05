from uuid import UUID
from pydantic import BaseModel

class SubjectResponseSchema(BaseModel):
    id: UUID
    name: str
    semester: str
    professor: str
