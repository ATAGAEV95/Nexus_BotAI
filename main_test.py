import asyncio
import os
import sys

import discord
from dotenv import load_dotenv


def check_imports() -> None:
    """Проверяет возможность импорта всех необходимых библиотек."""
    print("Проверка импортов...")
    try:
        import aiohttp  # noqa: F401
        import apscheduler  # noqa: F401
        import asyncpg  # noqa: F401
        import discord  # noqa: F401
        import sqlalchemy  # noqa: F401

        print("✅ Все необходимые библиотеки найдены.")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        sys.exit(1)


def check_env() -> None:
    """Проверяет наличие обязательных переменных окружения."""
    print("Проверка переменных окружения...")
    load_dotenv()

    required_vars = ["DC_TOKEN", "DATABASE_URL"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        print(f"❌ Отсутствуют переменные окружения: {', '.join(missing)}")
    else:
        print("✅ Все критические переменные окружения найдены.")


async def check_discord_connection() -> None:
    """Пытается установить соединение с Discord API для проверки токена."""
    print("Проверка подключения к Discord API...")
    token = os.getenv("DC_TOKEN_TEST") or os.getenv("DC_TOKEN")

    if not token:
        print("⚠️ Токен не найден, пропускаем проверку подключения к Discord.")
        return

    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f"✅ Успешное подключение к Discord как {client.user}")
        await client.close()

    @client.event
    async def on_error(event: str, *args: list, **kwargs: dict) -> None:
        print(f"❌ Ошибка при подключении к Discord: {event}")
        await client.close()
        sys.exit(1)

    try:
        await client.login(token)
        await client.connect(reconnect=False)
    except discord.LoginFailure:
        print("❌ Неверный токен Discord.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")
        sys.exit(1)


async def main() -> None:
    """Основная функция запуска Sanity Check."""
    print("=== Запуск проверки системы (Sanity Check) ===")
    check_imports()
    check_env()
    print("=== Проверка системы завершена успешно ===")


if __name__ == "__main__":
    asyncio.run(main())
