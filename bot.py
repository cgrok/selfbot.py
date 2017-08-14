import discord
from ext.formatter import EmbedHelp
from discord.ext import commands
from contextlib import redirect_stdout
import datetime
import json
import inspect
import os
import glob
import io
import textwrap
import traceback

def run_wizard():
    print('------------------------------------------')
    print('WELCOME TO THE VERIX-SELFBOT SETUP WIZARD!')
    print('------------------------------------------')
    token = input('Enter your token:\n> ')
    print('------------------------------------------')
    prefix = input('Enter a prefix for your selfbot:\n> ')
    data = {
        "BOT": {
            "TOKEN" : token,
            "PREFIX" : prefix
            },
        "FIRST" : False
        }
    with open('data/config.json','w') as f:
        f.write(json.dumps(data, indent=4))
    print('------------------------------------------')
    print('Successfully saved your data!')
    print('------------------------------------------')


with open('data/config.json') as f:
    if json.load(f)['FIRST']:
        run_wizard()

if 'TOKEN' in os.environ:
    heroku = True
    TOKEN = os.environ['TOKEN']
else:
    with open('data/config.json') as f:
        TOKEN = json.load(f)["BOT"]['TOKEN']

async def get_pre(bot, message):
    with open('data/config.json') as f:
        config = json.load(f)
    try:
        return config["BOT"]['PREFIX']
    except:
        return 's.'

bot = commands.Bot(command_prefix=get_pre, self_bot=True, formatter=EmbedHelp())
bot.remove_command('help')

_extensions = [

    'cogs.misc',
    'cogs.info',
    'cogs.utils',
    'cogs.mod'

    ]

@bot.event
async def on_ready():
    bot.uptime = datetime.datetime.now()
    print('------------------------------------------\n'
    	  'Self-Bot Ready\n'
    	  'Author: verix#7220\n'
    	  '------------------------------------------\n'
    	  'Username: {}\n'
          'User ID: {}\n'
          '------------------------------------------'
    	  .format(bot.user, bot.user.id))




@bot.command(pass_context=True)
async def ping(ctx):
    """Pong! Check your response time."""
    msgtime = ctx.message.timestamp.now()
    await (await bot.ws.ping())
    now = datetime.datetime.now()
    ping = now - msgtime
    pong = discord.Embed(title='Pong! Response Time:',
    					 description=str(ping.microseconds / 1000.0) + ' ms',
                         color=0x00ffff)

    await bot.say(embed=pong)

@bot.command(name='presence')
async def _set(Type=None,*,thing=None):
    """Change your discord game/stream!"""
    if Type is None:
            await bot.say('Usage: `.presence [game/stream] [message]`')
    else:
        if Type.lower() == 'stream':
            await bot.change_presence(game=discord.Game(name=thing,type=1,url='https://www.twitch.tv/a'),status='online')
            await bot.say('Set presence to. `Streaming {}`'.format(thing))
        elif Type.lower() == 'game':
            await bot.change_presence(game=discord.Game(name=thing))
            await bot.say('Set presence to `Playing {}`'.format(thing))
        elif Type.lower() == 'clear':
            await bot.change_presence(game=None)
            await bot.say('Cleared Presence')
        else:
            await bot.say('Usage: `.presence [game/stream] [message]`')

async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            print(page)
            await bot.send_message(ctx.message.channel, embed=page)
        print('Sent command help')
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            print(page)
            await bot.send_message(ctx.message.channel, embed=page)
        print('Sent command help')

@bot.event
async def on_command_error(error, ctx):
   print(error)
   channel = ctx.message.channel
   if isinstance(error, commands.MissingRequiredArgument):
       await send_cmd_help(ctx)
       print('Sent command help')
   elif isinstance(error, commands.BadArgument):
       await send_cmd_help(ctx)
       print('Sent command help')
   elif isinstance(error, commands.DisabledCommand):
       await bot.send_message(channel, "That command is disabled.")
       print('Command disabled.')
   elif isinstance(error, commands.CommandInvokeError):
       # A bit hacky, couldn't find a better way
       no_dms = "Cannot send messages to this user"
       is_help_cmd = ctx.command.qualified_name == "help"
       is_forbidden = isinstance(error.original, discord.Forbidden)
       if is_help_cmd and is_forbidden and error.original.text == no_dms:
           msg = ("I couldn't send the help message to you in DM. Either"
                  " you blocked me or you disabled DMs in this server.")
           await bot.send_message(channel, msg)
           return

@bot.command(pass_context=True)
async def coglist(ctx):
    def pagify(text, delims=["\n"], *, escape=True, shorten_by=8,
               page_length=2000):
        """DOES NOT RESPECT MARKDOWN BOXES OR INLINE CODE"""
        in_text = text
        if escape:
            num_mentions = text.count("@here") + text.count("@everyone")
            shorten_by += num_mentions
        page_length -= shorten_by
        while len(in_text) > page_length:
            closest_delim = max([in_text.rfind(d, 0, page_length)
                                 for d in delims])
            closest_delim = closest_delim if closest_delim != -1 else page_length
            if escape:
                to_send = escape_mass_mentions(in_text[:closest_delim])
            else:
                to_send = in_text[:closest_delim]
            yield to_send
            in_text = in_text[closest_delim:]


        yield in_text

    def box(text, lang=""):
        ret = "```{}\n{}\n```".format(lang, text)
        return ret
    loaded = [c.__module__.split(".")[1] for c in bot.cogs.values()]
    # What's in the folder but not loaded is unloaded
    def _list_cogs():
          cogs = [os.path.basename(f) for f in glob.glob("cogs/*.py")]
          return ["cogs." + os.path.splitext(f)[0] for f in cogs]
    unloaded = [c.split(".")[1] for c in _list_cogs()
                if c.split(".")[1] not in loaded]

    if not unloaded:
        unloaded = ["None"]

    msg = ("+ Loaded\n"
           "{}\n\n"
           "- Unloaded\n"
           "{}"
           "".format(", ".join(sorted(loaded)),
                     ", ".join(sorted(unloaded)))
           )
    for page in pagify(msg, [" "], shorten_by=16):
        await bot.say(box(page.lstrip(" "), lang="diff"))

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

@bot.command(pass_context=True, name='eval')
async def _eval(ctx, *, body: str):
    '''Run python scripts on discord!'''
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
        return await bot.say(get_syntax_error(e))

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await bot.say('```py\n{}{}\n```'.format(value, traceback.format_exc()))
    else:
        value = stdout.getvalue()
        try:
            await bot.add_reaction(ctx.message, '\u2705')
        except:
            pass

        if ret is None:
            if value:
                await bot.say('```py\n%s\n```' % value)
        else:

            await bot.say('```py\n%s%s\n```' % (value, ret))


@bot.command(pass_context=True,name='reload')
async def _reload(ctx,*, module : str):
    """Reloads a module."""
    channel = ctx.message.channel
    module = 'cogs.'+module
    try:
        bot.unload_extension(module)
        x = await bot.send_message(channel,'Successfully Unloaded.')
        bot.load_extension(module)
        x = await bot.edit_message(x,'Successfully Reloaded.')
    except Exception as e:
        x = await bot.edit_message(x,'\N{PISTOL}')
        await bot.say('{}: {}'.format(type(e).__name__, e))
    else:
        x = await bot.edit_message(x,'Done. \N{OK HAND SIGN}')

@bot.command(pass_context=True)
async def load(ctx, *, module):
    '''Loads a module.'''
    module = 'cogs.'+module
    try:
        bot.load_extension(module)
        await bot.say('Successfully Loaded.')
    except Exception as e:
        await bot.say('\N{PISTOL}\n{}: {}'.format(type(e).__name__, e))

@bot.command(pass_context=True)
async def unload(ctx, *, module):
    '''Unloads a module.'''
    module = 'cogs.'+module
    try:
        bot.unload_extension(module)
        await bot.say('Successfully Unloaded `{}`'.format(module))
    except:
        pass

for extension in _extensions:
    try:
        bot.load_extension(extension)
        print('Loaded: {}'.format(extension))
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Error on load: {}\n{}'.format(extension, exc))

try:
    bot.run(TOKEN, bot=False)
except Exception as e:
    print('\n[ERROR]: \n{}\n'.format(e))
