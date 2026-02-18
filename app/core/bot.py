import discord
from discord.ext import commands
import logging
import os
from .config import settings
# from app.data.models import async_session_maker # Будет добавлено позже
# from app.services.scheduler import setup_scheduler # Будет добавлено позже

logger = logging.getLogger(__name__)

class DisBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None, # Мы реализуем собственный help
            description="Nexus Bot AI"
        )
        
    async def setup_hook(self):
        logger.info("Загрузка когов...")
        # Загрузка когов из папки app/cogs
        for filename in os.listdir("./app/cogs"):
            if filename.endswith(".py") and filename != "__init__.py":
                try:
                    await self.load_extension(f"app.cogs.{filename[:-3]}")
                    logger.info(f"Ког {filename} успешно загружен")
                except Exception as e:
                    logger.error(f"Ошибка при загрузке кога {filename}: {e}")
        
        # Синхронизация команд
        try:
            synced = await self.tree.sync()
            logger.info(f"Синхронизировано {len(synced)} команд")
        except Exception as e:
            logger.error(f"Ошибка синхронизации команд: {e}")

    async def on_ready(self):
        logger.info(f"Бот запущен как {self.user} (ID: {self.user.id})")
        logger.info("------")
        
        # Здесь будет инициализация БД и шедулера
        # logger.info("Подключение к БД...")
        # logger.info("Запуск планировщика...")
        
    async def on_connect(self):
        logger.info("Бот подключился к Discord Gateway")

    async def on_disconnect(self):
        logger.info("Бот отключился от Discord Gateway")
