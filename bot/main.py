import discord
import asyncio
import aiohttp
import utils
import logging
import logging.config
import yaml
import os

from discord.ext import commands


with open('logging_config.yaml', 'r') as f:
    log_cfg = yaml.safe_load(f.read())
    logging.config.dictConfig(log_cfg)


logger = logging.getLogger('hqrBotLogger')

cogs = [
    'cogs.test',
]


headers = {
    'User-Agent':'hqrTestBot#0573 "A Discord bot"'
}

DC_TOKEN = os.environ['HQR_DC_TOKEN']

intents = discord.Intents(
    message_content=True,
    reactions=True,
    messages=True,
    members=True,
    guilds=True,
    emojis=True,
    bans=True
)


async def startup():
    config = utils.Config().load_json('config_test.json')
    default_prefixes = ['!', 'hqr.', 'hqr ']
    logger.info('Starting bot...')
    bot = utils.CustomBot(
        activity=discord.Activity(type=discord.ActivityType.watching, name="hqr.sh"),
        allowed_mentions=discord.AllowedMentions(replied_user=False),
        command_prefix=commands.when_mentioned_or(default_prefixes),
        strip_after_prefix=True,
        case_insensitive=True,
        max_messages=20000,
        intents=intents,
        config=config,
        owner_ids = set(config.admins),
    )
    logger.debug('Token: %s' % DC_TOKEN)

    bot.cogs_list = cogs
    for cog in cogs:
        logger.info(f'Loading cog: {cog}')
        await bot.load_extension(cog)

    async with aiohttp.ClientSession(headers=headers) as session:
        bot.session = session
        await bot.start(DC_TOKEN)

if __name__ == '__main__':
    asyncio.run(startup())
