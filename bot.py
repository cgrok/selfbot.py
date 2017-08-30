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

    def cleanup_code( content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(e):
        if e.text is None:
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    async def to_code_block(ctx, body):
        if body.startswith('```') and body.endswith('```'):
            content = '\n'.join(body.split('\n')[1:-1])
        else:
            content = body.strip('`')
        await ctx.message.edit(content='```py\n'+content+'```')

    @commands.command(name='eval')
    async def _eval(ctx, *, body: str):
        '''Run python scripts on discord!'''
        await to_code_block(ctx, body)
        env = {
            'bot': bot,
            'ctx': ctx,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'server': ctx.message.server,
            'message': ctx.message,
        }

        env.update(globals())

        body = cleanup_code(content=body)
        stdout = io.StringIO()

        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await ctx.send(get_syntax_error(e))

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            x = await ctx.send('```py\n{}{}\n```'.format(value, traceback.format_exc()))
            try:
                await x.add_reaction('\U0001f534')
            except:
                pass
        else:
            value = stdout.getvalue()

            if TOKEN in value:
                value = value.replace(TOKEN,"[EXPUNGED]")

            if ret is None:
                if value:
                    try:
                        x = await ctx.send('```py\n%s\n```' % value)
                    except:
                        x = await ctx.send('```py\n\'Result was too long.\'```')
                    try:
                        await x.add_reaction('\U0001f535')
                    except:
                        pass
                else:
                    try:
                        await ctx.message.add_reaction('\U0001f535')
                    except:
                        pass
            else:
                try:
                    x = await ctx.send('```py\n%s%s\n```' % (value, ret))
                except:
                    x = await ctx.send('```py\n\'Result was too long.\'```')
                try:
                    await x.add_reaction('\U0001f535')
                except:
                    pass
if __name__ == '__main__':
    SelfBot().run()
