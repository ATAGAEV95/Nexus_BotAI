import asyncio
import logging
from app.core.config import settings
from app.core.bot import DisBot
from app.data.models import init_db
from app.services.scheduler import setup_scheduler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Запуск Nexus Bot AI...")
    
    # Инициализация БД
    await init_db()
    
    # Инициализация бота
    bot = DisBot()
    
    # Запуск планировщика
    await setup_scheduler(bot)
    
    # Запуск бота
    async with bot:
        await bot.start(settings.DC_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем.")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")
