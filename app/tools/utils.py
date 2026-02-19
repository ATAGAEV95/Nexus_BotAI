import re
from datetime import datetime


def clean_content(content: str) -> str:
    """Очищает строку от нежелательных символов."""
    return content.strip()

def is_valid_url(url: str) -> bool:
    """Проверяет, является ли строка валидным URL."""
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def format_dt(dt: datetime, style: str = "f") -> str:
    """Форматирует дату для Discord (<t:timestamp:style>)."""
    return f"<t:{int(dt.timestamp())}:{style}>"
