from perplexity import AsyncPerplexity

from app.core.config import settings

client = AsyncPerplexity(api_key=settings.PERPLEXITY_API_KEY)


async def get_perplexity_answer(
    query: str, temperature: float = 0.2, system_message: str | None = None
) -> str:
    """Получает ответ от Perplexity AI (асинхронно)."""
    default_system = (
        "Be precise and concise. Answer in Russian. "
        "Do not use markdown formatting (bold, italics, headers, etc.). "
        "Keep the text clean and simple."
    )

    try:
        response = await client.chat.completions.create(
            model="sonar-reasoning-pro",
            messages=[
                {"role": "system", "content": system_message or default_system},
                {"role": "user", "content": query},
            ],
            temperature=temperature,
        )

        content = response.choices[0].message.content
        return str(content) if content else "Пустой ответ от AI."
    except Exception as e:
        return f"Ошибка при запросе к AI: {e}"


async def get_perplexity_search(query: str) -> str:
    """Выполняет поиск через Perplexity AI."""
    try:
        search = await client.search.create(
            query=query, country="RU", search_language_filter=["ru"], max_results=5
        )

        result_str = ""
        for result in search.results:
            result_str += f"{result.snippet}\n"
        return result_str
    except Exception as e:
        return f"Ошибка при запросе к AI: {e}"
