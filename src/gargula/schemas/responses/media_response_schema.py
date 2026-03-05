from uuid import UUID
from pydantic import BaseModel

class MediaResponseSchema(BaseModel):
    id: UUID
    key: str
    transcription: str
