from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str
    AZURE_BLOB_CONTAINER: str
    AZURE_BLOB_CONNECTION_STRING: str
    AZURE_OPENAI_API_KEY: str
    AZURE_ENDPOINT: str
    AZURE_EMBEDDING_MODEL_NAME: str
    AZURE_CHAT_MODEL_NAME: str
    QDRANT_HOST: str
    QDRANT_PORT: str

    class Config:
        env_file = ".env"

settings = Settings()
