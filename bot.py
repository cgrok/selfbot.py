import discord
from discord.ext import commands
import datetime


bot = commands.Bot(command_prefix='s.', self_bot=True)

_extensions = [

    'cogs.eval',
    'cogs.misc',
    'cogs.embed',
    'cogs.info'

    ]


@bot.event
async def on_ready():
    bot.uptime = datetime.datetime.now()
    print('--------------\n'
    	  'Self-Bot Ready\n'
    	  'Made by verix.\n'
    	  '--------------\n'
    	  'Logged in as: {}'
    	  .format(bot.user))



@bot.command(pass_context=True,description='Response time is in ms.')
async def ping(ctx):
    msgtime = ctx.message.timestamp.now()
    await (await bot.ws.ping())
    now = datetime.datetime.now()
    ping = now - msgtime
    pong = discord.Embed(title='Pong! Response Time:', 
    					 description=str(ping.microseconds / 1000.0) + ' ms',
                         color=0x00ffff)

    await bot.say(embed=pong)


@bot.command(aliases=['p'], pass_context=True)
async def purge(ctx, msgs: int, *, txt=None):
    await bot.delete_message(ctx.message)
    if msgs < 10000:
        async for message in bot.logs_from(ctx.message.channel, limit=msgs):
            try:
                if txt:
                    if txt.lower() in message.content.lower():
                        await bot.delete_message(message)
                else:
                    await bot.delete_message(message)
            except:
                pass
    else:
        await bot.send_message(ctx.message.channel, 'Too many messages to delete. Enter a number < 10000')


@bot.command(aliases=['c'], pass_context=True)
async def clean(ctx, msgs: int = 100):
    await bot.delete_message(ctx.message)
    if msgs < 10000:
        async for message in bot.logs_from(ctx.message.channel, limit=msgs):
            try:
                if message.author == bot.user:
                    await bot.delete_message(message)
            except:
                pass
    else:
        await bot.send_message(ctx.message.channel, 'Too many messages to delete. Enter a number < 10000')

if __name__ == "__main__":
    for extension in _extensions:
        try:
            bot.load_extension(extension)
            print('Loaded extension: {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run("MzE5Mzk1NzgzODQ3ODM3Njk2.DF2Klg.zEgTAzHvjaXYaRgY5puSWTsTbDk", bot=False)