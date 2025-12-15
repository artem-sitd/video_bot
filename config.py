from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file(local: bool = False) -> Path:
    return Path(__file__).parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=get_env_file(),
                                      env_file_encoding='utf-8')

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    BOT_TOKEN: str
    OPENAI_API_KEY: str

    @property
    def DATABASE_URL_async(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def DATABASE_URL_sync(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
