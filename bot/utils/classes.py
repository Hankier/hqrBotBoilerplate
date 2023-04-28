import datetime
import discord
import asyncio
import yaml
import os
import logging
import utils

from discord import Message, User
from discord.ext import commands, menus
from sqlalchemy import create_engine

from typing import Union, Optional, Dict, List

__all__ = [
    'CustomContext',
    'CustomBot',
]

logger = logging.getLogger('hqrBotLogger')


class CustomContext(commands.Context):
    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.bot: CustomBot = self.bot
        self.uncaught_error = False

    async def send(self, *args, **kwargs) -> Message:
        kwargs['reference'] = kwargs.get('reference', self.message.reference)

        return await super().send(*args, **kwargs)


class CustomBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cogs_list: List[str] = []
        self.fully_ready = False
        self.session = None
        self.synced = True
        config_file = kwargs.get('config_file', 'config_test.json')
        self.config = utils.Config().load_json(config_file)
        logger.debug('Config loaded %s', self.config)

    @staticmethod
    def get_custom_prefix(_bot: 'CustomBot', message: discord.Message):
        logger.debug('Getting prefix for message')
        default_prefixes = ['!', 'hqr.', 'hqr ']

        if _bot.config.prefixes:
            return commands.when_mentioned_or(*_bot.config.prefixes)(_bot, message)
        else:
            return commands.when_mentioned_or(*default_prefixes)(_bot, message)

    async def setup_hook(self):
        self.loop.create_task(self.startup())

    async def get_context(self, message: Message, *, cls=CustomContext) -> CustomContext:
        return await super().get_context(message, cls=cls)

    async def on_ready(self):
        logger.info('Logged in as %s (ID: %s)', self.user, self.user.id)
        await self.wait_until_ready()
        logger.info('Bot is ready.')
        if not self.synced:
            logger.debug('Syncing slash commands...')
            synced = await self.tree.sync()
            logger.debug("Synced {len(synced)} command(s)")
            self.synced = True

    async def on_message(self, message: Message):
        logger.debug('On message invoked')
        if not self.fully_ready:
            logger.debug('Bot is not fully ready. Waiting for fully_ready event...')
            await self.wait_for('fully_ready')

        if message.author.bot:
            logger.debug('Ignoring bot message.')
            return
        elif message.guild is None:
            logger.debug('Ignoring DM message.')
            return
        elif message.guild.id == self.config.guild:
            logger.debug('On message')
            await self.process_commands(message)
        else:
            logger.debug('Ignoring message from other guild. %s(%s)', message.guild, message.guild.id)

    async def startup(self):
        await self.wait_until_ready()

        #self.start_time: datetime = datetime.now(timezone.utc)
        self.fully_ready = True
        self.dispatch('fully_ready')
        logger.info('Bot is fully ready.')

    async def close(self):
        await super().close()

    async def get_owner(self) -> User:
        if not self.owner_id and not self.owner_ids:
            info = await self.application_info()
            self.owner_id = info.owner.id

        return await self.fetch_user(self.owner_id or list(self.owner_ids)[0])

