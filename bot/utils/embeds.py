import datetime
import discord
import logging
import time

__all__ = [
    'create_bot_permanent_embed',
    'create_log_embed',
]

BOT_VERSION = '0.0.1'
BOT_NAME = 'hqrTestBot'
BOT_LOGO = 'https://static-files.hqr.sh/hqr_gold_2.png'
HQR_LOGO = 'https://static-files.hqr.sh/hqr_logo_transparent.png'

logger = logging.getLogger('hqrBotLogger')

def create_bot_permanent_embed(title: str, description: str, color_str: str = '#f1d292') -> discord.Embed:
    logger.debug('Create bot embed')
    color = discord.Color.from_str(color_str)

    embed = discord.Embed(title=title, color=color)
    embed.description = description
    embed.set_thumbnail(url=HQR_LOGO)
    embed.set_author(name=BOT_NAME, icon_url=BOT_LOGO)

    logger.debug('Embed created')
    return embed

def create_log_embed(user: discord.User, title: str, description: str, color_str: str = '#f1d292') -> discord.Embed:
    logger.debug('Create log embed')
    color = discord.Color.from_str(color_str)

    embed = discord.Embed(title=title, color=color)
    embed.description = description
    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
    embed.timestamp = datetime.datetime.now()
    embed.set_footer(text=embed_footer_text(), icon_url=BOT_LOGO)
    return embed
