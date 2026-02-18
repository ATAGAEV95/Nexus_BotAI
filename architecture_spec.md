
# Универсальная Архитектура Discord Бота

Этот документ описывает архитектуру и структуру файлов для создания универсального, расширяемого Discord бота. Это шаблон для разработки чистых и поддерживаемых проектов.

## 1. Технический стек

*   **Язык**: Python 3.13+
*   **Пакетный менеджер**: `uv` (вместо pip/poetry).
*   **Фреймворк**:
    *   `discord.py` (v2.5+) — основной фреймворк.
*   **База данных**:
    *   PostgreSQL (драйвер `asyncpg`).
    *   `SQLAlchemy` (v2.0+) — асинхронная ORM.
*   **Асинхронность и Сеть**:
    *   `asyncio` — стандартная библиотека.
    *   `aiohttp` — для любых внешних HTTP запросов.
*   **Планировщик задач**:
    *   `APScheduler` (AsyncIOScheduler) — для фоновых задач (кронов).
*   **Инструменты разработки**:
    *   `ruff` — линтинг и форматирование.
    *   `pytest` + `pytest-asyncio` — тестирование.
    *   `python-dotenv` — управление конфигурацией.

## 2. Структура проекта

Проект следует модульной архитектуре. Ненужные зависимости (AI, RAG, и т.д.) удалены.

```text
project_root/
├── .agent/
│   └── rules/
│       └── russia.md        # Правила (язык, стек)
├── .env                     # Токены и секреты (в .gitignore)
├── .env.example             # Пример конфигурации
├── .gitignore
├── Dockerfile               # Production-ready образ
├── README.md                # Инструкция по запуску
├── main.py                  # Точка входа (Entrypoint)
├── main_test.py             # Скрипт проверки окружения и зависимостей (Pre-flight check)
├── pyproject.toml           # Конфигурация uv, ruff, pytest
├── uv.lock                  # Лок-файл зависимостей (uv)
├── app/
│   ├── __init__.py
│   ├── cogs/                # Модули с командами (Extensions)
│   │   ├── __init__.py
│   │   └── general.py       # Основные команды (!help, !ping)
│   ├── core/                # Ядро
│   │   ├── __init__.py
│   │   ├── bot.py           # Класс DisBot (наследник commands.Bot)
│   │   ├── config.py        # Загрузка и валидация конфига (pydantic или os.getenv)
│   │   └── embeds.py        # Утилиты для красивых ответов (Embeds)
│   ├── data/                # Слой данных
│   │   ├── __init__.py
│   │   ├── models.py        # ORM Модели и создание сессии (Engine/Session)
│   │   └── requests.py      # CRUD операции и запросы к БД
│   ├── services/            # Бизнес-логика и планировщик
│   │   ├── __init__.py
│   │   └── scheduler.py     # Настройка периодических задач
│   └── tools/               # Вспомогательные функции
│       ├── __init__.py
│       └── utils.py         # Форматирование, валидаторы и т.д.
└── tests/                   # Папка тестов
    ├── __init__.py
    ├── conftest.py          # Глобальные фикстуры (bot, db session)
    └── test_general.py      # Тесты команд
```

## 3. Детальное описание компонентов

### Core (`app/core`)

*   **`bot.py` (`DisBot`)**:
    *   Класс-наследник от `commands.Bot`.
    *   **Метод `setup_hook`**: Асинхронная загрузка когов (`app.cogs.*`) и синхронизация команд дерева (slash commands).
    *   **Метод `on_ready`**: Инициализация подключения к БД и запуск шедулера.
    *   Обработка жизненного цикла (подключение/отключение).
*   **`embeds.py`**:
    *   Содержит унифицированные стили для Embed-сообщений (успех, ошибка, информация).
    *   Реализует генерацию красивого `help` сообщения.
*   **`config.py`**:
    *   Централизованная загрузка переменных из `.env`. Валидация наличия критических токенов при старте.
*   **`main_test.py`**:
    *   Скрипт "здоровья" (Sanity Check), запускаемый перед основным ботом или в CI/CD.
    *   Проверяет наличие всех импортов (библиотек).
    *   Проверяет корректность `.env` (наличие токенов).
    *   Выполняет пробный запуск `discord.Client` с тестовым токеном (`DC_TOKEN_TEST`), чтобы убедиться в коннекте к API Discord.

### Data (`app/data`)

*   **`models.py`**:
    *   **Инфраструктура БД**: Создание `create_async_engine` и `async_sessionmaker`.
    *   **Base Model**: Базовая модель SQLAlchemy (`DeclarativeBase`).
    *   **Модели**:
        *   `User`: (id, join_date).
        *   `GuildSettings`: (id, prefix, settings).
*   **`requests.py` (DAL - Data Access Layer)**:
    *   Функции или классы для работы с БД.
    *   Пример: `get_user(user_id)`, `update_settings(guild_id, **kwargs)`.
    *   Изолирует код бота от прямых SQL-запросов.

### Services (`app/services`)

*   **`scheduler.py`**:
    *   Настройка `AsyncIOScheduler`.
    *   Пример задачи: очистка старых записей в БД или периодическая отправка напоминаний.
    *   Задачи должны быть обернуты в `try-except`, чтобы падение одной задачи не свалило планировщик.

### Cogs (`app/cogs`)

*   **`general.py`**:
    *   Базовые команды администрирования и утилиты.
    *   Команда `!help` (или `/help`), использующая стили из `embeds.py`.

## 4. Ключевые паттерны разработки

1.  **Пакетный менеджер `uv`**:
    *   Использовать `uv init`, `uv add discord.py sqlalchemy asyncpg aiohttp apscheduler` для инициализации.
    *   `uv run main.py` для запуска.
2.  **Асинхронность**:
    *   Все операции ввода-вывода (БД, API) строго асинхронные (`await`).
3.  **Dependency Injection (DI)**:
    *   Передавать пул коннектов к БД или сессию в команды через объект бота или контекст, а не создавать новые соединения в каждой функции.
4.  **Типизация**:
    *   Использовать `mypy` или встроенные type hints Python. 100% покрытие типов для новых функций.

## 5. Пример `pyproject.toml` (для uv)

```toml
[project]
name = "discord-bot-template"
version = "0.1.0"
description = "Universal Discord Bot Template"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "discord-py>=2.5.0",
    "sqlalchemy>=2.0.0",
    "asyncpg>=0.30.0",
    "python-dotenv>=1.0.0",
    "apscheduler>=3.10.0",
    "aiohttp>=3.9.0",
]

[tool.ruff]
line-length = 88
target-version = "py313"
```

## 6. Запуск проекта

1.  Установить `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2.  Установить зависимости: `uv sync`
3.  Создать `.env` из примера.
4.  Запустить: `uv run main.py`
