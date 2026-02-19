import discord
from discord.ext import commands

from app.core.handlers import get_perplexity_answer, get_perplexity_search
from app.tools.prompts import get_steam_free_games_prompt


class AI(commands.Cog):
    """Ког для функций ИИ."""

    def __init__(self, bot: commands.Bot) -> None:
        """Инициализация кога."""
        self.bot = bot

    @commands.command(name="steam")
    async def steam(self, ctx: commands.Context) -> None:
        """Поиск бесплатных игр в Steam."""
        async with ctx.typing():
            system_prompt, user_prompt = get_steam_free_games_prompt()
            response = await get_perplexity_answer(
                user_prompt, 
                temperature=0.1, 
                system_message=system_prompt
            )
            await self._send_response(ctx.message, response)

    async def _send_response(self, message: discord.Message, response: str) -> None:
        """Отправляет ответ в чат."""
        if len(response) <= 4096:
            embed = discord.Embed(description=response, color=discord.Color.blue())
            await message.reply(embed=embed)
        else:
            for i in range(0, len(response), 2000):
                await message.reply(response[i:i+2000])

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Обработчик сообщений для команд ИИ."""
        if message.author.bot:
            return

        if message.content.startswith("?"):
            # Проверяем, является ли сообщение командой бота
            ctx = await self.bot.get_context(message)
            if ctx.valid:
                return  # Если это команда, даем discord.py обработать её

            query = message.content[1:].strip()
            if not query:
                return

            async with message.channel.typing():
                response = await get_perplexity_answer(query)
                await self._send_response(message, response)

async def setup(bot: commands.Bot) -> None:
    """Функция загрузки кога."""
    await bot.add_cog(AI(bot))
