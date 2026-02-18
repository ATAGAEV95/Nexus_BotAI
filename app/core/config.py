import os
import logging
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        self.DC_TOKEN = os.getenv("DC_TOKEN")
        self.DC_TOKEN_TEST = os.getenv("DC_TOKEN_TEST")
        self.POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
        self.POSTGRES_DB = os.getenv("POSTGRES_DB", "nexus_bot")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
        self.APS_COALESCE_MS = int(os.getenv("APS_COALESCE_MS", "50"))

        self._validate()

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def _validate(self):
        if not self.DC_TOKEN:
            logger.critical("DC_TOKEN не найден в переменных окружения!")
            raise ValueError("DC_TOKEN is required")

settings = Config()
