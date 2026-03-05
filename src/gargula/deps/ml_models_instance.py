import whisper
from typing import Optional
from whisper import Whisper
from sentence_transformers import SentenceTransformer
from gargula.settings import settings

class MLModelsInstance:
    __embedding_model: Optional[SentenceTransformer] = None
    __stt_model: Optional[Whisper] = None

    @classmethod
    def get_embedding_model(cls) -> SentenceTransformer:
        if cls.__embedding_model is None:
            cls.__embedding_model = SentenceTransformer(settings.ml_embedding_model_name)
        return cls.__embedding_model

    @classmethod
    def get_stt_model(cls) -> Whisper:
        if cls.__stt_model is None:
            cls.__stt_model = whisper.load_model(settings.ml_stt_model_name)
        return cls.__stt_model
