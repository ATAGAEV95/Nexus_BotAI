import pytest
from unittest.mock import AsyncMock
from discord.ext import commands

@pytest.mark.asyncio
async def test_ping(bot):
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    
    cog = bot.get_cog("General")
    await cog.ping(ctx)
    
    ctx.send.assert_called_once()
    args, kwargs = ctx.send.call_args
    embed = kwargs.get('embed')
    assert embed.title == "✅ Pong!"

@pytest.mark.asyncio
async def test_help(bot):
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    
    cog = bot.get_cog("General")
    await cog.help_command(ctx)
    
    ctx.send.assert_called_once()
    args, kwargs = ctx.send.call_args
    embed = kwargs.get('embed')
    assert embed.title == "ℹ️ Помощь"
    # Проверяем, что есть поле General
    assert any(field.name == "General" for field in embed.fields)
