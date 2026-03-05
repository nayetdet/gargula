from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General
    cors_origin: str

    # Database
    database_user: str
    database_password: str
    database_host: str
    database_port: int
    database_name: str

    # S3
    s3_endpoint_url: str
    s3_access_key_id: str
    s3_secret_access_key: str
    s3_region: str
    s3_addressing_style: str
    s3_media_bucket: str

    # ML
    ml_embedding_model_name: str
    ml_stt_model_name: str

    @property
    def database_sync_url(self) -> str:
        return f"postgresql+psycopg://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

    @property
    def database_async_url(self) -> str:
        return f"postgresql+asyncpg://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

settings: Settings = Settings()
