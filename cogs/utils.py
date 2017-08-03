import discord
from discord.ext import commands
import asyncio
import requests
from bs4 import BeautifulSoup
from urllib import parse
from urllib.request import Request, urlopen
import traceback
import discord
import inspect
import textwrap
from contextlib import redirect_stdout
import io

class Utility:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    @commands.command(aliases=['nick'], pass_context=True, no_pm=True)
    async def nickname(self, ctx, *, nick):
        """Change your nickname on a server."""
        await self.bot.delete_message(ctx.message)
        try:
            await self.bot.change_nickname(ctx.message.author, nick)
            await self.bot.say('Changed nickname to: `{}`'.format(nick), delete_after=5)
        except:
            await self.bot.say('Unable to change nickname.', delete_after=5)

    @commands.command(pass_context=True)
    async def raw(self, ctx, ID, chan : discord.channel=None):
    	"""Get the raw content of someones message!"""
    	channel = channel or ctx.message.channel
    	await self.bot.delete_message(ctx.message)
    	msg = None
    	async for m in self.bot.logs_from(channel, limit=1000):
    		if m.id == ID:
    			msg = m
    			break
    	out = msg.content.replace('*','\\*').replace('`','\\`').replace('~~','\\~~').replace('_','\\_').replace('<','\\<').replace('>','\\>')
    	try:
    		await self.bot.say(out)
    	except:
    		await self.bot.say('Message too long.')


    @commands.command(pass_context=True)
    async def quote(self, ctx, id : str, chan : discord.Channel=None):
    	"""Quote someone's message by ID"""
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
    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    @commands.command(pass_context=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        '''Run python scripts on discord!'''
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'server': ctx.message.server,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await self.bot.say(self.get_syntax_error(e))

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await self.bot.say('```py\n{}{}\n```'.format(value, traceback.format_exc()))
        else:
            value = stdout.getvalue()
            try:
                await self.bot.add_reaction(ctx.message, '\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await self.bot.say('```py\n%s\n```' % value)
            else:
                self._last_result = ret
                await self.bot.say('```py\n%s%s\n```' % (value, ret))

    @commands.command(pass_context=True,description='Do .embed to see how to use it.')
    async def embed(self, ctx, *, msg: str = None):
        '''Embed complex rich embeds as the bot.'''
        try:
            
            if msg:
                ptext = title = description = image = thumbnail = color = footer = author = None
                timestamp = discord.Embed.Empty
                def_color = False
                embed_values = msg.split('|')
                for i in embed_values:
                    if i.strip().lower().startswith('ptext='):
                        if i.strip()[6:].strip() == 'everyone':
                            ptext = '@everyone'
                        elif i.strip()[6:].strip() == 'here':
                            ptext = '@here'
                        else:
                            ptext = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('title='):
                        title = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('description='):
                        description = i.strip()[12:].strip()
                    elif i.strip().lower().startswith('desc='):
                        description = i.strip()[5:].strip()
                    elif i.strip().lower().startswith('image='):
                        image = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('thumbnail='):
                        thumbnail = i.strip()[10:].strip()
                    elif i.strip().lower().startswith('colour='):
                        color = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('color='):
                        color = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('footer='):
                        footer = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('author='):
                        author = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('timestamp'):
                        timestamp = ctx.message.timestamp

                    if color:
                        if color.startswith('#'):
                            color = color[1:]
                        if not color.startswith('0x'):
                            color = '0x' + color

                    if ptext is title is description is image is thumbnail is color is footer is author is None and 'field=' not in msg:
                        await self.bot.delete_message(ctx.message)
                        return await self.bot.send_message(ctx.message.channel, content=None,
                                                           embed=discord.Embed(description=msg))

                    if color:
                        em = discord.Embed(timestamp=timestamp, title=title, description=description, color=int(color, 16))
                    else:
                        em = discord.Embed(timestamp=timestamp, title=title, description=description)
                    for i in embed_values:
                        if i.strip().lower().startswith('field='):
                            field_inline = True
                            field = i.strip().lstrip('field=')
                            field_name, field_value = field.split('value=')
                            if 'inline=' in field_value:
                                field_value, field_inline = field_value.split('inline=')
                                if 'false' in field_inline.lower() or 'no' in field_inline.lower():
                                    field_inline = False
                            field_name = field_name.strip().lstrip('name=')
                            em.add_field(name=field_name, value=field_value.strip(), inline=field_inline)
                    if author:
                        if 'icon=' in author:
                            text, icon = author.split('icon=')
                            if 'url=' in icon:
                                print("here")
                                em.set_author(name=text.strip()[5:], icon_url=icon.split('url=')[0].strip(), url=icon.split('url=')[1].strip())
                            else:
                                em.set_author(name=text.strip()[5:], icon_url=icon)
                        else:
                            if 'url=' in author:
                                print("here")
                                em.set_author(name=author.split('url=')[0].strip()[5:], url=author.split('url=')[1].strip())
                            else:
                                em.set_author(name=author)

                    if image:
                        em.set_image(url=image)
                    if thumbnail:
                        em.set_thumbnail(url=thumbnail)
                    if footer:
                        if 'icon=' in footer:
                            text, icon = footer.split('icon=')
                            em.set_footer(text=text.strip()[5:], icon_url=icon)
                        else:
                            em.set_footer(text=footer)
                await self.bot.send_message(ctx.message.channel, content=ptext, embed=em)
            else:
                msg = '*Params:*\n```bf\n[title][author][desc][field][footer][thumbnail][image][timestamp][ptext]```'
                await self.bot.send_message(ctx.message.channel, msg)
            try:
                await self.bot.delete_message(ctx.message)
            except:
                pass
        except:
            await self.bot.send_message(ctx.message.channel, 'looks like something fucked up. or i dont have embed perms')
               
            
def setup(bot):
	bot.add_cog(Utility(bot))

