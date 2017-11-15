import discord
from discord.ext import commands
import asyncio
from colorthief import ColorThief
from urllib.parse import urlparse
import io
import os
import base64

class CustomContext(commands.Context):
    '''Custom Context class to provide utility.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session(self):
        '''Returns the bot's aiohttp client session'''
        return self.bot.session

    def delete(self):
        '''shortcut'''
        return self.message.delete()

    async def get_ban(self, name_or_id):
        '''Helper function to retrieve a banned user'''
        for ban in await self.guild.bans():
            if name_or_id.isdigit():
                if ban.user.id == int(name_or_id):
                    return ban
            if name_or_id.lower() in str(ban.user).lower():
                return ban

    async def purge(self, *args, **kwargs):
        '''Shortcut to channel.purge, preset for selfbots.'''
        kwargs.setdefault('bulk', False)
        await self.channel.purge(*args, **kwargs)

    async def _get_message(self, channel, id):
        '''Goes through channel history to get a message'''
        async for message in channel.history(limit=2000):
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
        falsy = ['n', 'no', 'false','0','fuck off','f']
        if resp.content.lower().strip() in falsy:
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

    @staticmethod
    def is_valid_image_url(url):
        '''Checks if a url leads to an image.'''
        types = ['.png', '.jpg', '.gif', '.bmp', '.webp']
        parsed = urlparse(url)
        if any(parsed.path.endswith(i) for i in types):
            return url.replace(parsed.query, 'size=128')

    async def get_dominant_color(self, url=None, quality=10):
        '''Returns the dominant color of an image from a url'''
        maybe_col = os.environ.get('COLOR')

        url = url or self.author.avatar_url

        if maybe_col:
            raw = int(maybe_col.strip('#'), 16)
            return discord.Color(value=raw)

        if not self.is_valid_image_url(url):
            raise ValueError('Invalid image url passed.')
        try:
            async with self.session.get(url) as resp:
                image = await resp.read()
        except:
            return discord.Color.default()

        with io.BytesIO(image) as f:
            try:
                color = ColorThief(f).get_color(quality=quality)
            except:
                return discord.Color.dark_grey()
            
        return discord.Color.from_rgb(*color)

    async def success(self, msg=None, delete=False):
        if delete:
            await self.message.delete()
        if msg:
            await self.send(msg)
        else:
            await self.message.add_reaction('✅')

    async def failure(self, msg=None):
        if msg:
            await self.send(msg)
        else:
            await self.message.add_reaction('⁉')

    
    async def updatedata(self, path:str, content:str, commitmsg='No Commit Message'):
        '''To edit data in Github'''
        git = self.bot.get_cog('Git')
        #get username
        username = await git.githubusername()
        #get sha (dont even know why this is a compulsory field)
        async with self.session.get(f'https://api.github.com/repos/{username}/selfbot.py/contents/{path}', headers={"Authorization": f"Bearer {git.githubtoken}"}) as resp2:
            if 300 > resp2.status >= 200:
                #push to path
                async with self.session.put(f'https://api.github.com/repos/{username}/selfbot.py/contents/{path}', headers={"Authorization": f"Bearer {git.githubtoken}"}, json={"path":"data/cc.json", "message":commitmsg, "content":base64.b64encode(bytes(content, 'utf-8')).decode('ascii'), "sha":(await resp2.json())['sha'], "branch":"rewrite"}) as resp3:
                    if 300 > resp3.status >= 200:
                        return True
                        #data pushed successfully
                    else:
                        await self.send('Well, I failed somehow, send the following to `4JR#2713` (180314310298304512): ```py\n' + str(await resp3.json()) + '\n```')
                        return False 
            else:
                await self.send('Well, I failed somehow, send the following to `4JR#2713` (180314310298304512): ```py\n' + str(await resp2.json()) + '\n```')
                return False

    @staticmethod
    def paginate(text: str):
        '''Simple generator that paginates text.'''
        last = 0
        pages = []
        for curr in range(0, len(text)):
            if curr % 1980 == 0:
                pages.append(text[last:curr])
                last = curr
                appd_index = curr
        if appd_index != len(text)-1:
            pages.append(text[last:curr])
        return list(filter(lambda a: a != '', pages))
