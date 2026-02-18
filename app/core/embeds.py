import discord
from discord.ext import commands

class Embeds:
    @staticmethod
    def success(title: str, description: str) -> discord.Embed:
        return discord.Embed(
            title=f"✅ {title}",
            description=description,
            color=discord.Color.green()
        )

    @staticmethod
    def error(title: str, description: str) -> discord.Embed:
        return discord.Embed(
            title=f"❌ {title}",
            description=description,
            color=discord.Color.red()
        )

    @staticmethod
    def info(title: str, description: str) -> discord.Embed:
        return discord.Embed(
            title=f"ℹ️ {title}",
            description=description,
            color=discord.Color.blue()
        )

    @staticmethod
    def warning(title: str, description: str) -> discord.Embed:
        return discord.Embed(
            title=f"⚠️ {title}",
            description=description,
            color=discord.Color.orange()
        )
