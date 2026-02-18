from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(url=settings.database_url)
    },
    job_defaults={
        'coalesce': True,
        'max_instances': 1,
        'misfire_grace_time': settings.APS_COALESCE_MS
    }
)

async def setup_scheduler(bot):
    logger.info("Запуск планировщика...")
    scheduler.start()
    logger.info("Планировщик запущен.")
