from typing import List
from gargula.models.media import Media
from gargula.schemas.responses.media_response_schema import MediaResponseSchema

class MediaMapper:
    @staticmethod
    def to_model(key: str, transcription: str, embedding: List[float]) -> Media:
        return Media(
            key=key,
            transcription=transcription,
            embedding=embedding
        )

    @staticmethod
    def to_response_schema(media: Media) -> MediaResponseSchema:
        return MediaResponseSchema(
            id=media.id,
            key=media.key,
            transcription=media.transcription
        )
