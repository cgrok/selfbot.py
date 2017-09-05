import discord
from discord.ext import commands
import asyncio

class CustomContext(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session(self):
        return self.bot.session

    async def _get_message(self, channel, id):
        async for message in channel.history(limit=10000):
            if message.id == id:
                return message

    async def get_message(self, channel_or_id, id=None):
        '''Helper tool to get a message for selfbots'''
        if isinstance(channel_or_id, int):
            msg = await self._get_message(channel=self.channel, id=channel_or_id)
        else:
            msg = await self._get_message(channel=channel_or_id, id=id)
        return msg


		
