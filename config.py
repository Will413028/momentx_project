from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    container_name: str
    connection_string: str

    class Config:
        env_file = ".env"
