import discord

from app.core.bot import DisBot
from app.core.config import settings

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


def main() -> None:
    """Запуск бота."""
    bot = DisBot(
        command_prefix="?",
        intents=intents,
        help_command=None,
    )

    if not settings.DC_TOKEN:
        print("Ошибка: DC_TOKEN не найден в переменных окружения!")
        return

    bot.run(settings.DC_TOKEN)


if __name__ == "__main__":
    main()
