from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    container_name: str
    connection_string: str
    database_url: str
    AZURE_OPENAI_API_KEY: str
    AZURE_ENDPOINT: str
    AZURE_EMBEDDING_MODEL_NAME: str

    class Config:
        env_file = ".env"
