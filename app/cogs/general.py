from discord.ext import commands

from app.core.embeds import Embeds


class General(commands.Cog):
    """Основные команды бота."""

    def __init__(self, bot: commands.Bot) -> None:
        """Инициализация кога."""
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """Проверка задержки бота."""
        latency = round(self.bot.latency * 1000)
        embed = Embeds.info("Pong!", f"Задержка: {latency}мс")
        await ctx.send(embed=embed)

    @commands.command(name="help")
    async def help_command(self, ctx: commands.Context) -> None:
        """Показывает список доступных команд."""
        embed = Embeds.info("Помощь", "Список доступных команд:")

        for cog_name, cog in self.bot.cogs.items():
            command_list = ""
            for command in cog.get_commands():
                if not command.hidden:
                    command_list += f"`?{command.name}` - {command.help}\n"

            if command_list:
                embed.add_field(name=cog_name, value=command_list, inline=False)

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Загрузка кога в бота."""
    await bot.add_cog(General(bot))
