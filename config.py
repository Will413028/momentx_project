from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    test_env: str

    class Config:
        env_file = ".env"
