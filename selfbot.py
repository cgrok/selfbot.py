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

default_data = {
    "PREFIX": "r.",
    "TOKEN": "your_token_here",
    }

def run_wizard():
    print('------------------------------------------')
    print('WELCOME TO THE VERIXX-SELFBOT SETUP WIZARD!')
    print('------------------------------------------')
    token = input('Enter your token:\n> ')
    print('------------------------------------------')
    prefix = input('Enter a prefix for your selfbot:\n> ')
    data = {
        "PREFIX": prefix,
        "TOKEN": token
        }
    with open('data/config.json','w') as f:
        f.write(json.dumps(data, indent=4))
    print('------------------------------------------')
    print('Successfully saved your data!')
    print('------------------------------------------')

if 'TOKEN' in os.environ:
    heroku = True
    TOKEN = os.environ['TOKEN']
else:
    heroku = False
    with open('data/config.json') as f:
        if json.load(f)["TOKEN"] == default_data["TOKEN"]:
            run_wizard()
    with open('data/config.json') as f:
        TOKEN = json.load(f)['TOKEN']

async def get_pre(bot, message):
    if 'PREFIX' in os.environ:
        return os.environ['PREFIX']

    with open('data/config.json') as f:
        config = json.load(f)
    try:
        return config['PREFIX']
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
    print(textwrap.dedent(f"""
    ------------------------------------------
    Self-Bot Ready
    Author: verix#7220
    ------------------------------------------
    Username: {bot.user}
    User ID: {bot.user.id}
    ------------------------------------------"""))
    await bot.change_presence(status=discord.Status.invisible, afk=True)


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

@bot.command(pass_context=True)
async def shutdown(ctx):
    """Restarts the selfbot."""
    channel = ctx.message.channel
    await bot.say("Shutting down...")
    await bot.logout()

@bot.command(name='presence')
async def _set(Type,*,message=None):
    """Change your discord game/stream!"""
    if Type.lower() == 'stream':
        await bot.change_presence(game=discord.Game(name=message,type=1,url=f'https://www.twitch.tv/{message}'),status='online')
        await bot.say(f'Set presence to. `Streaming {message}`')
    elif Type.lower() == 'game':
        await bot.change_presence(game=discord.Game(name=message))
        await bot.say(f'Set presence to `Playing {message}`')
    elif Type.lower() == 'clear':
        await bot.change_presence(game=None)
        await bot.say('Cleared Presence')
    else:
        await bot.say('Usage: `.presence [game/stream/clear] [message]`')

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
    '''See unloaded and loaded cogs!'''
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
        ret = f"```{lang}\n{text}\n```"
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

    em1 = discord.Embed(color=discord.Color.green(), title="+ Loaded", description=", ".join(sorted(loaded)))
    em2 = discord.Embed(color=discord.Color.red(), title="- Unloaded", description=", ".join(sorted(unloaded)))
    await bot.say(embed=em1)
    await bot.say(embed=em2)

def cleanup_code( content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    # remove `foo`
    return content.strip('` \n')

def get_syntax_error(e):
    if e.text is None:
        return f'```py\n{e.__class__.__name__}: {e}\n```'
    return f'```py\n{e.text}'^':>{e.offset}\n{type(e).__name__}: {e}```'

async def to_code_block(ctx, body):
    if body.startswith('```') and body.endswith('```'):
        content = '\n'.join(body.split('\n')[1:-1])
    else:
        content = body.strip('`')
    await bot.edit_message(ctx.message, '```py\n'+content+'```')

@bot.command(pass_context=True, name='eval')
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
        return await bot.say(get_syntax_error(e))

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        x = await bot.say(f'```py\n{e}\n{traceback.format_exc()}\n{value}```')
        try:
            await bot.add_reaction(x, '\U0001f534')
        except:
            pass
    else:
        value = stdout.getvalue()

        if TOKEN in value:
            value = value.replace(TOKEN,"[EXPUNGED]")


        if ret is None:
            if value:
                try:
                    x = await bot.say('```py\n%s\n```' % value)
                except:
                    x = await bot.say('```py\n\'Result was too long.\'```')
                try:
                    await bot.add_reaction(x, '\U0001f535')
                except:
                    pass
            else:

                try:
                    await bot.add_reaction(ctx.message, '\U0001f535')
                except:
                    pass
        else:
            if TOKEN in ret:
                ret = ret.replace(TOKEN,"[EXPUNGED]")
            try:
                x = await bot.say('```py\n%s%s\n```' % (value, ret))
            except:
                x = await bot.say('```py\n\'Result was too long.\'```')
            try:
                await bot.add_reaction(x, '\U0001f535')
            except:
                pass

@bot.command(pass_context=True)
async def say(ctx, *, message: str):
    '''Say something as the bot.'''
    if f'{ctx.prefix}say' in message:
        await bot.say("Don't ya dare spam.")
    else:
        await bot.say(message)

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
        await bot.say(f'{type(e).__name__}: {e}')
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
        await bot.say(f'\N{PISTOL}\n{type(e).__name__}: {e}')

@bot.command(pass_context=True)
async def unload(ctx, *, module):
    '''Unloads a module.'''
    module = 'cogs.'+module
    try:
        bot.unload_extension(module)
        await bot.say(f'Successfully Unloaded `{module}`')
    except:
        pass

for extension in _extensions:
    try:
        bot.load_extension(extension)
        print(f'Loaded: {extension}')
    except Exception as e:
        exc = f'{type(e).__name__}: {e}'
        print(f'Error on load: {extension}\n{exc}')

try:
    bot.run(TOKEN.strip('\"'), bot=False)
except Exception as e:
    print(f'\n[ERROR]: \n{e}\n')
