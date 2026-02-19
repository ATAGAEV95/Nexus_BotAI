import discord
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

DB_TIMEOUT = 10

def start_scheduler(bot: discord.Client) -> None:
    """Инициализирует и запускает асинхронный планировщик задач."""
    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Moscow"))
    scheduler.start()
