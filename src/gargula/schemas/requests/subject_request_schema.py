from pydantic import BaseModel, Field

class SubjectRequestSchema(BaseModel):
    name: str = Field(min_length=1)
    semester: str = Field(min_length=1)
    professor: str = Field(min_length=1)
