import discord
from discord.ext import commands
import asyncio
import io
from colorthief import ColorThief

class CustomContext(commands.Context):
    '''Custom Context class to provide utility.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session(self):
        '''Returns the bot's aiohttp client session'''
        return self.bot.session

    async def _get_message(self, channel, id):
        '''Goes through channel history to get a message'''
        history = await channel.history(limit=5000).flatten()
        for message in history:
            if message.id == id:
                return message

    async def get_message(self, channel_or_id, id=None):
        '''Helper tool to get a message for selfbots'''
        if isinstance(channel_or_id, int):
            msg = await self._get_message(channel=self.channel, id=channel_or_id)
        else:
            msg = await self._get_message(channel=channel_or_id, id=id)
        return msg

    async def confirm(self, msg):
        '''Small helper for confirmation messages.'''
        await self.send(msg or '*Are you sure you want to proceed?* `(Y/N)`')
        resp = self.bot.wait_for('message', check=lambda m: m == ctx.author)
        truthy = ['n', 'no', 'noo']
        if resp.content.lower().strip() in truthy:
            return False
        else:
            return True

    async def send_cmd_help(self):
        '''Sends command help'''
        if self.invoked_subcommand:
            pages = self.formatter.format_help_for(self, self.invoked_subcommand)
            for page in pages:
                await self.send_message(self.message.channel, page)
        else:
            pages = self.formatter.format_help_for(self, self.command)
            for page in pages:
                await self.send_message(self.message.channel, page)


    async def get_dominant_color(self, url):
        '''Returns the dominant color of an image from a url'''
        if url is None:
            return 0x000000

        async with self.session.get(url) as resp:
            image = await resp.read()

        with io.BytesIO(image) as f:
            color = ColorThief(f).get_color(quality=1)

        return discord.Color.from_rgb(*color)




		
