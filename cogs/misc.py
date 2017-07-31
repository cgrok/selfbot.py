import discord
from discord.ext import commands
import datetime
import time
import random
import asyncio
import json
import requests
import os

class Misc():


    def __init__(self, bot):
        self.bot = bot
        self.ball = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes definitely', 'You may rely on it',
                     'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
                     'Reply hazy try again',
                     'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
                     'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good',
                     'Very doubtful']
        self.selfroles = ['Subscriber','Hype']

    async def send_cmd_help(self,ctx):
        if ctx.invoked_subcommand:
            pages = self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)
        else:
            pages = self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)

    @commands.command(pass_context=True)
    async def embedsay(self,ctx, *, message: str = None):
        '''Embed something as the bot.'''
        color = ("#%06x" % random.randint(8, 0xFFFFFF))
        color = int(color[1:],16)
        color = discord.Color(value=color)
        if message:
            msg = ctx.message
            emb = discord.Embed(color=color,description=message)
            await self.bot.delete_message(msg)
            await self.bot.say(embed=emb)
        else:
            await self.bot.say('Usage: `.embedsay [message]`')


    @commands.command()
    async def say(self,*, message: str):
        '''Say something as the bot.'''
        if '@everyone' in message:
            await self.bot.say('Not so fast cheeky boi xdd')
        elif '@here' in message:
            await self.bot.say('Ayy lmao, it doesnt work.')
        else:       
            await self.bot.say(message)

            
    @commands.command()
    async def add(self,*args):
        '''Add multiple numbers.'''
        ans = 0
        try:
            for i in args:
                ans += int(i)
            await self.bot.say(ans)
        except:
            await self.bot.say('Enter numbers only.')
            


#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------


    @commands.command(pass_context=True)
    async def virus(self,ctx,user: discord.Member=None,*,hack=None):
        """Inject a virus into someones system."""
        nome = ctx.message.author
        if not hack:
            hack = 'discord'
        else:
            hack = hack.replace(' ','_')
        channel = ctx.message.channel
        x = await self.bot.send_message(channel, '``[▓▓▓                    ] / {}-virus.exe Packing files.``'.format(hack))
        await asyncio.sleep(1.5)
        x = await self.bot.edit_message(x,'``[▓▓▓▓▓▓▓                ] - {}-virus.exe Packing files..``'.format(hack))
        await asyncio.sleep(0.3)
        x = await self.bot.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓           ] \ {}-virus.exe Packing files...``'.format(hack))
        await asyncio.sleep(1.2)
        x = await self.bot.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {}-virus.exe Initializing code.``'.format(hack))
        await asyncio.sleep(1)
        x = await self.bot.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {}-virus.exe Initializing code..``'.format(hack))
        await asyncio.sleep(1.5)
        x = await self.bot.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {}-virus.exe Finishing.``'.format(hack))
        await asyncio.sleep(1)
        x = await self.bot.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] \ {}-virus.exe Finishing..``'.format(hack))
        await asyncio.sleep(1)
        x = await self.bot.edit_message(x,'``Successfully downloaded {}-virus.exe``'.format(hack))
        await asyncio.sleep(2)
        x = await self.bot.edit_message(x,'``Injecting virus.   |``')
        await asyncio.sleep(0.5)
        x = await self.bot.edit_message(x,'``Injecting virus..  /``')
        await asyncio.sleep(0.5)
        x = await self.bot.edit_message(x,'``Injecting virus... -``')
        await asyncio.sleep(0.5)
        x = await self.bot.edit_message(x,'``Injecting virus....\``')
        await self.bot.delete_message(x)
        await self.bot.delete_message(ctx.message)
        
        if user:
            await self.bot.say('`{}-virus.exe` successfully injected into **{}**\'s system.'.format(hack,user.name))
            await self.bot.send_message(user,'**Alert!**\n``You may have been hacked. {}-virus.exe has been found in your system\'s operating system.\nYour data may have been compromised. Please re-install your OS immediately.``'.format(hack))
        else:
            await self.bot.say('**{}** has hacked himself ¯\_(ツ)_/¯.'.format(name.name))
            await self.bot.send_message(name,'**Alert!**\n``You may have been hacked. {}-virus.exe has been found in your system\'s operating system.\nYour data may have been compromised. Please re-install your OS immediately.``'.format(hack))
     
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

        
    @commands.command(pass_context=True, aliases=['8ball'])
    async def ball8(self, ctx, *, msg : str):
        """Let the 8ball decide your fate."""
        answer = random.randint(0, 19)
        
        if answer < 10:
            color = 0x008000
        elif 10 <= answer < 15:
            color = 0xFFD700
        else:
            color = 0xFF0000
        em = discord.Embed(color=color)
        em.add_field(name='\u2753 Question', value=msg)
        em.add_field(name='\ud83c\udfb1 8ball', value=self.ball[answer], inline=False)
        await self.bot.send_message(ctx.message.channel, content=None, embed=em)
        await self.bot.delete_message(ctx.message)




    @commands.command(pass_context=True, aliases=['emote','e'])
    async def emoji(self, ctx, *, msg):
        """
        Embed or copy a custom emoji (from any server).
        Usage:
        1) >emoji :smug: [Will display the smug emoji as an image]
        2) >emoji copy :smug: [Will add the emoji as a custom emote for the server]
        """
        copy_emote_bool = False
        if "copy " in msg:
            msg = msg.split("copy ")[1]
            copy_emote_bool = True
        if msg.startswith('s '):
            msg = msg[2:]
            get_server = True
        else:
            get_server = False
        msg = msg.strip(':')
        if msg.startswith('<'):
            msg = msg[2:].split(':', 1)[0].strip()
        url = emoji = server = None
        exact_match = False
        for server in self.bot.servers:
            for emoji in server.emojis:
                if msg.strip().lower() in str(emoji):
                    url = emoji.url
                    emote_name = emoji.name
                if msg.strip() == str(emoji).split(':')[1]:
                    url = emoji.url
                    emote_name = emoji.name
                    exact_match = True
                    break
            if exact_match:
                break
        response = requests.get(emoji.url, stream=True)
        name = emoji.url.split('/')[-1]
        with open(name, 'wb') as img:

            for block in response.iter_content(1024):
                if not block:
                    break

                img.write(block)

        if url:
            try:
                if get_server:
                    await self.bot.send_message(ctx.message.channel,
                                                '**ID:** {}\n**Server:** {}'.format(emoji.id, server.name))
                with open(name, 'rb') as fp:
                    if copy_emote_bool:
                        e = fp.read()
                    else:
                        await self.bot.send_file(ctx.message.channel, fp)
                if copy_emote_bool:
                    try:
                        await self.bot.create_custom_emoji(ctx.message.server, name=emote_name, image=e)
                        embed = discord.Embed(title="Added new emote", color=discord.Color.blue())
                        embed.description = "New emote added: " + emote_name
                        await self.bot.say("", embed=embed)
                    except:
                        await self.bot.say("Not enough permissions to do this")
                os.remove(name)
            except:
                await self.bot.send_message(ctx.message.channel, url)
        else:
            await self.bot.send_message(ctx.message.channel, 'Could not find emoji.')

        return await self.bot.delete_message(ctx.message)



    
def setup(bot):
    bot.add_cog(Misc(bot))