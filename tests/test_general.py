from typing import cast
from unittest.mock import AsyncMock, PropertyMock, patch

import pytest
from discord.ext import commands

from app.cogs.general import General


@pytest.mark.asyncio
async def test_ping(bot: commands.Bot) -> None:
    """Тест команды ping."""
    ctx = AsyncMock()
    ctx.send = AsyncMock()

    with patch.object(commands.Bot, "latency", new_callable=PropertyMock) as mock_latency:
        mock_latency.return_value = 0.05
        cog = cast(General, bot.get_cog("General"))
        await cog.ping(ctx)

    ctx.send.assert_called_once()
    args, kwargs = ctx.send.call_args
    embed = kwargs.get("embed")
    assert embed.title == "ℹ️ Pong!"


@pytest.mark.asyncio
async def test_help(bot: commands.Bot) -> None:
    """Тест команды help."""
    ctx = AsyncMock()
    ctx.send = AsyncMock()

    cog = cast(General, bot.get_cog("General"))
    await cog.help_command(ctx)

    ctx.send.assert_called_once()
    args, kwargs = ctx.send.call_args
    embed = kwargs.get("embed")
    assert embed.title == "ℹ️ Помощь"
    # Проверяем, что есть поле General
    assert any(field.name == "General" for field in embed.fields)
