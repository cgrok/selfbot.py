import discord
from discord.ext import commands
import asyncio
import requests
from bs4 import BeautifulSoup
from urllib import parse
from urllib.request import Request, urlopen

class Utility:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['nick'], pass_context=True, no_pm=True)
    async def nickname(self, ctx, *, nick):
        """Change your nickname on a server. Leave empty to remove nick."""
        await self.bot.delete_message(ctx.message)
        try:
            await self.bot.change_nickname(ctx.message.author, nick)
            await self.bot.say('Changed nickname to: `{}`'.format(nick), delete_after=5)
        except:
            await self.bot.say('Unable to change nickname.', delete_after=5)

    @commands.command(pass_context=True)
    async def quote(self, ctx, id : str, chan : discord.Channel=None):
    	channel = chan or ctx.message.channel
    	await self.bot.delete_message(ctx.message)
    	msg = None
    	async for message in self.bot.logs_from(channel, limit=1000):
    		if message.id == id:
    			msg = message
    			break
    	if msg is None:
    		await self.bot.say('Could not find the message.')
    		return
    	auth = msg.author
    	channel = msg.channel
    	ts = msg.timestamp

    	em = discord.Embed(color=0x00FFFF,description=msg.clean_content,timestamp=ts)
    	em.set_author(name=str(auth),icon_url=auth.avatar_url or auth.default_avatar_url)
    	em.set_footer(text='#'+channel.name)

    	await self.bot.say(embed=em)

    @commands.command(pass_context=True, aliases=['yt', 'vid', 'video'])
    async def youtube(self, ctx, *, msg):
        """Search for videos on YouTube."""
        search = parse.quote(msg)
        response = requests.get("https://www.youtube.com/results?search_query={}".format(search)).text
        result = BeautifulSoup(response, "lxml")
        url="**Result:**\nhttps://www.youtube.com{}".format(result.find_all(attrs={'class': 'yt-uix-tile-link'})[0].get('href'))

        await self.bot.send_message(ctx.message.channel, url)







def setup(bot):
	bot.add_cog(Utility(bot))

