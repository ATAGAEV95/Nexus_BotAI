from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, JSON, DateTime, func
from datetime import datetime
from app.core.config import settings

# Создание асинхронного движка
engine = create_async_engine(settings.database_url, echo=False)

# Фабрика сессий
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    join_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class GuildSettings(Base):
    __tablename__ = "guild_settings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    prefix: Mapped[str] = mapped_column(default="!")
    settings: Mapped[dict] = mapped_column(JSON, default={})

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
