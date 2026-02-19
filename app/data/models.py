import os

from dotenv import load_dotenv
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SCHEMA = "public"


def get_engine(schema: str) -> create_async_engine:
    """Создает и возвращает асинхронный движок SQLAlchemy с указанной схемой."""
    return create_async_engine(
        str(DATABASE_URL),
        connect_args={"server_settings": {"search_path": schema}},
        pool_pre_ping=True,
    )


if SCHEMA is None or SCHEMA == "":
    engine = get_engine("public")
else:
    engine = get_engine(SCHEMA)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для всех моделей, поддерживающий асинхронные атрибуты."""

    pass


class User(Base):
    """Модель пользователя Discord."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    name = Column(String(50), nullable=False)
    context = Column(JSONB)
    datetime_insert = Column(DateTime, default=func.now())


class SteamSubscription(Base):
    """Модель подписки на раздачи Steam."""

    __tablename__ = "steam_subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(BigInteger, nullable=False)
    channel_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)


class SteamGame(Base):
    """Модель разосланных игр Steam."""

    __tablename__ = "steam_games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())


async def init_models() -> None:
    """Создает таблицы в базе данных, если они не существуют."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
