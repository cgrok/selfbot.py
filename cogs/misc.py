import discord
from discord.ext import commands

class Misc:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def echo(self, ctx, *, msg):
		await ctx.send(msg)

def setup(bot):
	bot.add_cog(Misc(bot))