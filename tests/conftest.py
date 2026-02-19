import discord
import pytest_asyncio
from discord.ext import commands

from app.cogs.general import General


@pytest_asyncio.fixture
async def bot() -> commands.Bot:
    """Фикстура для создания экземпляра бота с загруженным когом General."""
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)
    await bot.add_cog(General(bot))
    return bot
