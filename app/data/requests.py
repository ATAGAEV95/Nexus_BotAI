from sqlalchemy import select, update
from app.data.models import async_session_maker, User, GuildSettings
from sqlalchemy.dialects.postgresql import insert

async def get_user(user_id: int) -> User | None:
    async with async_session_maker() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def add_user(user_id: int) -> User:
    async with async_session_maker() as session:
        stmt = insert(User).values(id=user_id).on_conflict_do_nothing().returning(User)
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one()

async def get_guild_settings(guild_id: int) -> GuildSettings | None:
    async with async_session_maker() as session:
        stmt = select(GuildSettings).where(GuildSettings.id == guild_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def update_guild_settings(guild_id: int, **kwargs):
    async with async_session_maker() as session:
        stmt = update(GuildSettings).where(GuildSettings.id == guild_id).values(**kwargs)
        await session.execute(stmt)
        await session.commit()
