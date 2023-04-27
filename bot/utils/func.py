import time
import datetime
import discord
import logging
import utils

from typing import Union, Any, Callable, Tuple, List, Coroutine, Optional

__all__ = [
    'create_embed',
    'chunks',
    'fix_url',
    'handle_user_interaction_error',
    'chunk_string',
]

logger = logging.getLogger('hqrBotLogger')


def fix_url(url: Any):
    if not url:
        return None

    return str(url)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def chunk_string(data: str, size: int) -> List[str]:
    """Yield successive 1024-sized chunks from data."""
    for i in range(0, len(data), size):
        yield data[i:i + size]

async def handle_user_interaction_error(interaction: discord.Interaction, error: Exception, code: str) -> None:
        logger.debug('Handling user interaction error')
        logger.exception(error)
        guild = interaction.guild
        conf = interaction.client.config

        log_channel = guild.get_channel(conf.channels.log)
        support_channel = guild.get_channel(conf.channels.support)

        em_log = utils.create_log_error_embed(
                user=interaction.user,
                description=f'Wystąpił błąd podczas wykonywania komendy przez użytkownika {interaction.user.mention} ({interaction.user.id})',
                )
        em_log.add_field(name='Error', value=error)

        logger.debug(f'Sending log to {log_channel}')
        await log_channel.send(embed=em_log)

        embed = utils.create_bot_response_error_embed(
            title='Wystąpił błąd !',
            description=f'Coś poszło nie tak. Zgłoś się na {support_channel.mention} i opisz swoją sytuację.'
            )
        embed.add_field(name='Kod błędu', value=code)

        await interaction.response.send_message(embed=embed, ephemeral=True)

def create_embed(user: Optional[Union[discord.Member, discord.User]], *, image=None, thumbnail=None, **kwargs) -> discord.Embed:
    """Makes a discord.Embed with options for image and thumbnail URLs, and adds a footer with author name"""

    kwargs['color'] = kwargs.get('color', discord.Color.green())

    embed = discord.Embed(**kwargs)
    embed.set_image(url=fix_url(image))
    embed.set_thumbnail(url=fix_url(thumbnail))

    if user:
        embed.set_footer(text=f'Command sent by {user}', icon_url=fix_url(user.display_avatar))

    return embed

