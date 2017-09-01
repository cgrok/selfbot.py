import discord
from discord.ext import commands
import asyncio
from __main__ import p

class Utility:
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
	bot.add_cog(Utility(bot))

