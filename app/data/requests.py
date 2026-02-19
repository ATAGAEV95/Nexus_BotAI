import asyncio
from collections.abc import Callable
from functools import wraps
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import SteamGame, SteamSubscription, async_session

DB_TIMEOUT = 10


def db_operation(operation_name: str) -> Callable:
    """Декоратор для устранения бойлерплейта БД-операций.

    Оборачивает функцию в async with session + try/except с таймаутом.
    Декорируемая функция должна принимать session: AsyncSession первым аргументом.
    """

    def decorator(func_inner: Callable) -> Callable:
        @wraps(func_inner)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            async with async_session() as session:
                try:
                    return await asyncio.wait_for(
                        func_inner(session, *args, **kwargs), timeout=DB_TIMEOUT
                    )
                except TimeoutError:
                    raise Exception(f"Таймаут при {operation_name}.")
                except Exception as e:
                    if isinstance(e, (ValueError, Exception)) and "Таймаут" in str(e):
                        raise
                    raise Exception(f"Ошибка при {operation_name}: {e}")

        return wrapper

    return decorator


@db_operation("добавлении подписки на Steam")
async def add_steam_subscription(
    session: AsyncSession, server_id: int, channel_id: int
) -> SteamSubscription:
    """Добавляет или обновляет подписку на рассылку Steam раздач."""
    stmt = select(SteamSubscription).where(
        SteamSubscription.server_id == server_id, SteamSubscription.channel_id == channel_id
    )
    result = await session.execute(stmt)
    subscription = result.scalar_one_or_none()

    if subscription:
        subscription.is_active = True  # type: ignore
    else:
        subscription = SteamSubscription(server_id=server_id, channel_id=channel_id)
        session.add(subscription)

    await session.commit()
    return subscription


@db_operation("проверке игры Steam")
async def is_game_new_and_save(session: AsyncSession, game_name: str) -> bool:
    """Если игры (по имени) нет в БД — сохраняет и возвращает True. Иначе False."""
    stmt = select(SteamGame.name).where(SteamGame.name == game_name)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        return False
    session.add(SteamGame(name=game_name))
    await session.commit()
    return True


@db_operation("получении списка каналов для рассылки")
async def get_active_steam_subscriptions(session: AsyncSession) -> list[int]:
    """Возвращает список ID каналов, подписанных на раздачи."""
    stmt = select(SteamSubscription.channel_id).where(SteamSubscription.is_active.is_(True))
    result = await session.execute(stmt)
    return list(result.scalars().all())
