import discord
from discord.ext import commands
from ext.context import CustomContext
import datetime
import aiohttp
import json
import os
import sys
import traceback

class SelfBot(commands.Bot):
    def __init__(self, **attrs):
        super().__init__(command_prefix=self.get_pre, self_bot=True)

        self.session = aiohttp.ClientSession(loop=self.loop)
        self._extensions = [x.rstrip('.py') for x in os.listdir('cogs')]
        self.add_command(self.ping) 

        for extension in self._extensions:
            try:
                self.load_extension('cogs.'+extension)
                print('Loaded: {}'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Load error: {}\n{}'.format(extension, exc))

    @property
    def token(self):
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
        with open('data/config.json') as f:
            prefix = json.load(f).get('PREFIX')
        return os.environ.get('PREFIX') or prefix or 's.'

    @staticmethod
    def run_wizard():
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
        try:
            super().run(self.token.strip('\"'), bot=False, reconnect=True)
        except Exception as e:
            print('[Error] {}: {}'.format(type(e).__name__, e))

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.now()
        print('SelfBot Online!')
        print('Author: verixx#7220')
        print('Name: {}'.format(self.user))
        print('ID: {}'.format(self.user.id))

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=CustomContext)
        if ctx.command is None:
            return
        await self.invoke(ctx)

    async def on_message(self, message):
        if message.author.id != self.user.id:
            return
        await self.process_commands(message)

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
    SelfBot().run()
