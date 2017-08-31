import discord
from discord.ext import commands
from ext.context import CustomContext
import datetime
import time
import aiohttp
import json
import os
import sys
import asyncio

class SelfBot(commands.Bot):
    '''
    Custom Client for selfbot.py - Made by verix#7220
    '''
    def __init__(self, **attrs):
        super().__init__(command_prefix=self.get_pre, self_bot=True)
        self.session = aiohttp.ClientSession(loop=self.loop)
        self._extensions = [x.rstrip('.py') for x in os.listdir('cogs') if x.endswith('.py')]
        self.last_message = None
        self.presence_task = self.loop.create_task(self.presence_change())
        self.add_command(self.ping)

        for extension in self._extensions:
            try:
                self.load_extension('cogs.'+extension)
                print('Loaded: {}'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('[LoadError]: {}\n{}'.format(extension, exc))

    @property
    def token(self):
        '''Returns your token wherever it is'''
        with open('data/config.json') as f:
            config = json.load(f)
            if config.get('FIRST'):
                if not os.environ.get('TOKEN'):
                    self.run_wizard()
            else:
                token = config.get('TOKEN').strip('\"')
        return os.environ.get('TOKEN') or token

    @staticmethod
    async def get_pre(bot, message):
        '''Returns the prefix.'''
        with open('data/config.json') as f:
            prefix = json.load(f).get('PREFIX')
        return os.environ.get('PREFIX') or prefix or 's.'

    @staticmethod
    def run_wizard():
        '''Wizard for first start'''
        print('------------------------------------------')
        token = input('Enter your token:\n> ')
        print('------------------------------------------')
        prefix = input('Enter a prefix for your selfbot:\n> ')
        data = {
                "TOKEN" : token,
                "PREFIX" : prefix,
                "FIRST" : False
            }
        with open('data/config.json','w') as f:
            f.write(json.dumps(data, indent=4))
        print('------------------------------------------')
        print('Restarting...')
        print('------------------------------------------')
        os.execv(sys.executable, ['python'] + sys.argv)

    def run(self):
        '''Starts the actual bot'''
        try:
            super().run(self.token.strip('\"'), bot=False, reconnect=True)
        except Exception as e:
            print('[Error] {}: {}'.format(type(e).__name__, e))

    async def on_ready(self):
        '''Bot startup, sets uptime.'''
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.now()
        print('---------------')
        print('selfbot.py online!')
        print('---------------')
        print('Author: verixx#7220')
        print('---------------')
        print('Logged in as: {}'.format(self.user))
        print('User ID: {}'.format(self.user.id))
        print('---------------')

    async def process_commands(self, message):
        '''Utilises the CustomContext subclass of discord.Context'''
        ctx = await self.get_context(message, cls=CustomContext)
        if ctx.command is None:
            return
        await self.invoke(ctx)

    async def on_message(self, message):
        '''Responds only to yourself'''
        if message.author.id != self.user.id:
            return
        self.last_message = time.time()
        await self.process_commands(message)

    async def presence_change(self):
        '''
        Background task that changes your presence. 
        Useful if you are hosting the bot 24/7
        Your client must be on invisible mode for this to work
        '''
        await self.wait_until_ready()
        while not self.is_closed():
            if self.last_message:
                diff = time.time() - self.last_message
                if diff < 300:
                    await self.change_presence(status=discord.Status.online)
                elif diff > 300 and diff < 1800:
                    await self.change_presence(status=discord.Status.idle)
                elif diff > 1800:
                    await self.change_presence(status=discord.Status.invisible)
            await asyncio.sleep(10)

    @commands.command()
    async def ping(self, ctx):
        """Pong! Check your response time."""
        msgtime = ctx.message.created_at
        now = datetime.datetime.now()
        ping = now - msgtime
        pong = discord.Embed(title='Pong! Response Time:',
                             description=str(ping.microseconds / 1000.0) + ' ms',
                             color=0x00ffff)
        await ctx.send(embed=pong)

if __name__ == '__main__':
    bot = SelfBot()
    bot.run()
