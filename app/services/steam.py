import xml.etree.ElementTree as ET
from datetime import date, timedelta
from email.utils import parsedate_to_datetime

import aiohttp


async def fetch_rss(url: str) -> str:
    """Получает содержимое RSS-ленты по URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


def parse_rss(xml_content: str) -> list[str]:
    """Парсит XML и возвращает подходящие названия игр."""
    root = ET.fromstring(xml_content)
    channel = root.find("channel")
    if channel is None:
        channel = root

    valid_titles = []
    today = date.today()
    yesterday = today - timedelta(days=1)

    for item in channel.findall("item"):
        title_elem = item.find("title")
        if title_elem is None:
            continue

        title = title_elem.text
        if title and " (Steam)" in title:
            title = title.split(" (Steam)")[0]

        if not title:
            title = ""

        description_elem = item.find("description")
        description = ""
        if description_elem is not None and description_elem.text is not None:
            description = description_elem.text

        if description and "DLC" in description:
            continue

        pub_date_elem = item.find("pubDate")
        pub_date_str = pub_date_elem.text if pub_date_elem is not None else ""

        if pub_date_str:
            try:
                dt = parsedate_to_datetime(pub_date_str)
                if dt.date() in (today, yesterday):
                    valid_titles.append(title)
            except (ValueError, TypeError):
                continue

    return valid_titles


async def get_free_steam_games() -> list[str]:
    """Получает список бесплатных раздач Steam на сегодня и вчера."""
    url = "https://www.gamerpower.com/rss/steam"
    try:
        xml_content = await fetch_rss(url)
        return parse_rss(xml_content)
    except Exception as e:
        print(f"Ошибка при получении игр из Steam RSS: {e}")
        return []
