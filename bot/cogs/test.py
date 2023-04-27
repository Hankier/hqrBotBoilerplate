import discord
import utils
import logging

from discord.ext import commands

logger = logging.getLogger('hqrBotLogger')

class TestCog(commands.Cog, name='Test'):

    def __init__(self, bot: utils.CustomBot):
        self.bot: utils.CustomBot = bot

    @commands.is_owner()
    @commands.command(name='test')
    async def test(self, ctx: utils.CustomContext) -> None:
        logger.debug(f'Test called by {ctx.author} in {ctx.channel}')
        guild = ctx.message.guild
        await ctx.send('Working')


async def setup(bot):
    logger.info('Setup TestCog :: Start')
    await bot.add_cog(TestCog(bot))
    logger.info('Setup TestCog :: End')

