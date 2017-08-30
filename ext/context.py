import discord
from discord.ext import commands
import asyncio

class CustomContext(commands.Context):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	@property
	def session(self):
		return self.bot.session
		
