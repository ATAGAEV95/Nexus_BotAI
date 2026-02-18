import asyncio
import logging
import os
import sys
import discord
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SanityCheck")

def check_imports():
    logger.info("Проверка импортов...")
    try:
        import discord
        import sqlalchemy
        import asyncpg
        import aiohttp
        import apscheduler
        logger.info("✅ Все необходимые библиотеки найдены.")
    except ImportError as e:
        logger.critical(f"❌ Ошибка импорта: {e}")
        sys.exit(1)

def check_env():
    logger.info("Проверка переменных окружения...")
    load_dotenv()
    
    required_vars = ["DC_TOKEN", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        logger.critical(f"❌ Отсутствуют переменные окружения: {', '.join(missing)}")
        # Не выходим, так как это может быть запущено в CI без полного env, но предупреждаем
    else:
        logger.info("✅ Все критические переменные окружения найдены.")

async def check_discord_connection():
    logger.info("Проверка подключения к Discord API...")
    token = os.getenv("DC_TOKEN_TEST") or os.getenv("DC_TOKEN")
    
    if not token:
        logger.warning("⚠️ Токен не найден, пропускаем проверку подключения к Discord.")
        return

    client = discord.Client(intents=discord.Intents.default())
    
    @client.event
    async def on_ready():
        logger.info(f"✅ Успешное подключение к Discord как {client.user}")
        await client.close()

    @client.event
    async def on_error(event, *args, **kwargs):
        logger.critical(f"❌ Ошибка при подключении к Discord: {event}")
        await client.close()
        sys.exit(1)

    try:
        await client.login(token)
        await client.connect(reconnect=False)
    except discord.LoginFailure:
        logger.critical("❌ Неверный токен Discord.")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"❌ Ошибка соединения: {e}")
        sys.exit(1)

async def main():
    logger.info("=== Запуск проверки системы (Sanity Check) ===")
    check_imports()
    check_env()
    # await check_discord_connection() # Можно включить при необходимости, но требует валидный токен
    logger.info("=== Проверка системы завершена успешно ===")

if __name__ == "__main__":
    asyncio.run(main())
