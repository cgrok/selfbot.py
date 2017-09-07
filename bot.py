'''
MIT License

Copyright (c) 2017 verixx

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import discord
from discord.ext import commands
from ext.context import CustomContext
from collections import defaultdict
import datetime
import time
import aiohttp
import json
import os
import sys
import asyncio

class Selfbot(commands.Bot):
    '''
    Custom Client for selfbot.py - Made by verix#7220
    '''
    def __init__(self, **attrs):
        super().__init__(command_prefix=self.get_pre, self_bot=True)
        self.session = aiohttp.ClientSession(loop=self.loop)
        self._extensions = [x.replace('.py', '') for x in os.listdir('cogs') if x.endswith('.py')]
        self.last_message = None
        self.presence_task = self.loop.create_task(self.presence_change())
        self.commands_used = defaultdict(int)
        self.messages_sent = 0
        self.add_command(self.ping)
        self.add_command(self._logout)

        for extension in self._extensions:
            try:
                self.load_extension('cogs.'+extension)
                print('Loaded extension: {}'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('LoadError: {}\n{}'.format(extension, exc))

    @property
    def token(self):
        '''Returns your token wher≈≈ever it is'''
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

    @classmethod
    def init(bot, token=None):
        '''Starts the actual bot'''
        selfbot = bot()
        safe_token = token or selfbot.token.strip('\"')
        try:
            selfbot.run(safe_token, bot=False, reconnect=True)
        except Exception as e:
            print('[Error] {}: {}'.format(type(e).__name__, e))

    async def on_ready(self):
        '''Bot startup, sets uptime.'''
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.now()
        print('---------------')
        print('selfbot.py connected!')
        print('---------------')
        print('author: verixx#7220')
        print('---------------')
        print('logged in as: {}'.format(self.user))
        print('user id: {}'.format(self.user.id))
        print('---------------')

    async def on_command(self, ctx):
        cmd = ctx.command.qualified_name.replace(' ', '_')
        self.commands_used[cmd] += 1

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
        self.messages_sent += 1
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
                    await self.change_presence(status=discord.Status.online, afk=False)
                elif diff > 300 and diff < 1800:
                    await self.change_presence(status=discord.Status.idle, afk=True)
                elif diff > 1800:
                    await self.change_presence(status=discord.Status.invisible, afk=True)
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

    @commands.command(name='logout')
    async def _logout(self, ctx):
        await ctx.send('`Selfbot Logging out...`')
        await self.logout()

if __name__ == '__main__':
    Selfbot.init()
