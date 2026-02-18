import discord
from discord.ext import commands
from app.core.embeds import Embeds
import logging

logger = logging.getLogger(__name__)

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("General Cog загружен")

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Проверка задержки бота."""
        latency = round(self.bot.latency * 1000)
        embed = Embeds.info("Pong!", f"Задержка: {latency}мс")
        await ctx.send(embed=embed)

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Показывает список доступных команд."""
        embed = Embeds.info("Помощь", "Список доступных команд:")
        
        for cog_name, cog in self.bot.cogs.items():
            command_list = ""
            for command in cog.get_commands():
                if not command.hidden:
                    command_list += f"`!{command.name}` - {command.help}\n"
            
            if command_list:
                embed.add_field(name=cog_name, value=command_list, inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
