from discord.ext import commands

from app.core.checks import admin_or_owner
from app.core.embeds import Embeds


class Admin(commands.Cog):
    """Административные команды."""

    def __init__(self, bot: commands.Bot) -> None:
        """Инициализация Cog."""
        self.bot = bot

    @commands.command(name="steam")
    @commands.guild_only()
    @admin_or_owner()
    async def steam(self, ctx: commands.Context) -> None:
        """Показывает текущие бесплатные раздачи в Steam."""
        from app.services.steam import get_free_steam_games

        games = await get_free_steam_games()
        if not games:
            embed = Embeds.info("Steam Раздачи", "Раздач на сегодня от Steam нету.")
        else:
            description = "\n".join(f"• {game}" for game in games)
            embed = Embeds.info("Бесплатные раздачи Steam", description)

        await ctx.send(embed=embed)

    @commands.command(name="set_steam")
    @commands.guild_only()
    @admin_or_owner()
    async def set_steam_channel(self, ctx: commands.Context) -> None:
        """Устанавливает текущий канал для уведомлений о раздачах Steam."""
        from app.data.requests import add_steam_subscription

        if not ctx.guild:
            embed = Embeds.error("Ошибка", "Эта команда доступна только на серверах.")
            await ctx.send(embed=embed)
            return

        server_id = ctx.guild.id
        channel_id = ctx.channel.id

        try:
            await add_steam_subscription(server_id=server_id, channel_id=channel_id)  # type: ignore
            embed = Embeds.success(
                "Успех", "Этот канал успешно установлен для получения бесплатных раздач Steam!"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = Embeds.error("Ошибка", f"Произошла ошибка при сохранении: {e}")
            await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Загрузка Cog в бота."""
    await bot.add_cog(Admin(bot))
