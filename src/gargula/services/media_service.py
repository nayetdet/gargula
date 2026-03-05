import os
import tempfile
import aiofiles
from uuid import UUID
from typing import List, Set, Optional
from fastapi import UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
from gargula.deps.ml_models_instance import MLModelsInstance
from gargula.exceptions.media_exceptions import MediaNotFoundException
from gargula.mappers.media_mapper import MediaMapper
from gargula.models.media import Media
from gargula.repositories.media_repository import MediaRepository
from gargula.schemas.responses.media_response_schema import MediaResponseSchema
from gargula.services.s3_service import S3Service
from gargula.settings import settings

class MediaService:
    __BUCKET_NAME: str = settings.s3_media_bucket
    __ALLOWED_EXTENSIONS: Set[str] = {
        ".mp3",
        ".wav",
        ".m4a",
        ".aac",
        ".flac",
        ".ogg",
        ".oga",
        ".opus",
        ".webm",
        ".mp4",
        ".mkv",
        ".mov",
        ".avi",
    }

    @classmethod
    async def create(cls, session: AsyncSession, media_file: UploadFile) -> MediaResponseSchema:
        key: str = await S3Service.upload(bucket=cls.__BUCKET_NAME, file=media_file, allowed_extensions=cls.__ALLOWED_EXTENSIONS)
        try:
            transcription: str = await cls.__transcribe(media_file)
            embedding: List[float] = MLModelsInstance.get_embedding_model().encode(transcription).tolist()
            media: Media = await MediaRepository.create(session, MediaMapper.to_model(key, transcription, embedding))
            return MediaMapper.to_response_schema(media)
        except Exception:
            await S3Service.delete(bucket=cls.__BUCKET_NAME, key=key)
            raise

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, media_id: UUID) -> None:
        media: Optional[Media] = await MediaRepository.find_by_id(session, media_id)
        if media is None:
            raise MediaNotFoundException()
        await MediaRepository.delete(session, media)
        await S3Service.delete(bucket=cls.__BUCKET_NAME, key=media.key)

    @staticmethod
    async def __transcribe(media_file: UploadFile) -> str:
        await media_file.seek(0)
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath: str = os.path.join(tmpdir, media_file.filename)
            async with aiofiles.open(filepath, "wb") as file:
                while chunk := await media_file.read(1024 * 1024):
                    await file.write(chunk)
            return MLModelsInstance.get_stt_model().transcribe(filepath)["text"]
