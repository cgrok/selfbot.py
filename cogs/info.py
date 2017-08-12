import discord
from discord.ext import commands
import datetime
import time
import random
import asyncio
import json

class Info():


    def __init__(self, bot):
        self.bot = bot
         


    @commands.command(pass_context=True,aliases=['s','serverinfo','si'], no_pm=True)
    async def server(self, ctx):
        '''See information about the server.'''
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle or
                      m.status == discord.Status.dnd])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))
        colour = ("#%06x" % random.randint(0, 0xFFFFFF))
        colour = int(colour[1:], 16)

        data = discord.Embed(
            description=created_at,
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)

        if server.icon_url:
            data.set_author(name=server.name, icon_url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)
            print(data.to_dict())

        try:
            await self.bot.say(embed=data)
            
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")
    
    @commands.command(pass_context=True,no_pm=True,aliases=["ri","role"])
    async def roleinfo(self, ctx, *, role: discord.Role=None):
        '''Shows information about a role'''
        server = ctx.message.server

        if not role:
            role = server.default_role

        since_created = (ctx.message.timestamp - role.created_at).days
        role_created = role.created_at.strftime("%d %b %Y %H:%M")
        created_on = "{}\n({} days ago!)".format(role_created, since_created)

        users = len([x for x in server.members if role in x.roles])
        if str(role.colour) == "#000000":
            colour = "default"
            color = ("#%06x" % random.randint(0, 0xFFFFFF))
            color = int(colour[1:], 16)
        else:
            colour = "Hex: {}\nRGB: {}".format(str(role.colour).upper(),str(role.colour.to_tuple()))
            color = role.colour

        em = discord.Embed(colour=color)
        em.set_author(name=role.name)
        em.add_field(name="ID", value=role.id, inline=True)
        em.add_field(name="Users", value=users, inline=True)
        em.add_field(name="Mentionable", value=role.mentionable, inline=True)
        em.add_field(name="Hoist", value=role.hoist, inline=True)
        em.add_field(name="Position", value=role.position, inline=True)
        em.add_field(name="Managed", value=role.managed, inline=True)
        em.add_field(name="Colour", value=colour, inline=False)
        em.set_footer(text=created_on)

        try:
            await self.bot.say(embed=em)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

        
    @commands.command(pass_context=True,aliases=['ui','user'],description='See user-info of someone.')
    async def userinfo(self,ctx, user: discord.Member = None):
        '''See information about a user or yourself.'''
        server = ctx.message.server
        if user:
            pass
        else:
            user = ctx.message.author
        avi = user.avatar_url
        if avi:
            pass
        else:
            avi = user.default_avatar_url
        roles = sorted([x.name for x in user.roles if x.name != "@everyone"])
        if roles:
            roles = ', '.join(roles)
        else:
            roles = 'None'
        time = ctx.message.timestamp
        desc = '{0} is chilling in {1} mode.'.format(user.name,user.status)
        member_number = sorted(server.members,key=lambda m: m.joined_at).index(user) + 1
        em = discord.Embed(colour=0x00fffff,description = desc,timestamp=time)
        em.add_field(name='Nick', value=user.nick, inline=True)
        em.add_field(name='Member No.',value=str(member_number),inline = True)
        em.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y'))
        em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y'))
        em.add_field(name='Roles', value=roles, inline=True)
        em.set_footer(text='User ID: '+str(user.id))
        em.set_thumbnail(url=avi)
        em.set_author(name=user, icon_url='http://site-449644.mozfiles.com/files/449644/logo-1.png')
        try:
            await self.bot.say(embed=em)
            
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True,aliases=['av','dp'])
    async def avatar(self,ctx, user: discord.Member = None):
        '''Returns ones avatar URL'''
        if not user:
            user = ctx.message.author
        if not user.avatar_url:
            avi = user.default_avatar_url
        else:
            avi = user.avatar_url.replace("?size=1024","?size=2048").replace(".webp",".png")
            if ".gif" in avi:
                avi += "&f=.gif"
        colour = ("#%06x" % random.randint(0, 0xFFFFFF))
        colour = int(colour[1:], 16)
        em = discord.Embed(color=colour)
        em.set_image(url=avi)
        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name
        em.set_author(name=name, url=user.avatar_url)
        await self.bot.say(embed=em)


    @commands.command(pass_context=True)
    async def info(self, ctx):
        '''See bot information, uptime, servers etc.'''
        uptime = (datetime.datetime.now() - self.bot.uptime)
        hours, rem = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        days, hours = divmod(hours, 24)
        if days:
            time_ = '%s days, %s hours, %s minutes, and %s seconds' % (days, hours, minutes, seconds)
        else:
            time_ = '%s hours, %s minutes, and %s seconds' % (hours, minutes, seconds)
        servers = len(self.bot.servers)
        version = '0.1.1'
        library = 'discord.py'
        creator = 'verix#7220'
        discord_ = '[Support Server](https://discord.gg/wkPy3sb)'
        github = '[/verixx/selfbot](https://github.com/verixx/selfbot)'
        time = ctx.message.timestamp
        emb = discord.Embed(colour=0x00FFFF)
        emb.set_author(name='selfbot.py', icon_url=self.bot.user.avatar_url)
        emb.add_field(name='Version',value=version)
        emb.add_field(name='Library',value=library)
        emb.add_field(name='Creator',value=creator)
        emb.add_field(name='Servers',value=servers)
        emb.add_field(name='Github',value=github)
        emb.add_field(name='Discord',value=discord_)
        emb.add_field(name='Uptime',value=time_)
        emb.set_footer(text="ID: {}".format(self.bot.user.id))
        emb.set_thumbnail(url='https://cdn.discordapp.com/avatars/319395783847837696/349677f658e864c0a5247a658df61eb1.webp?width=80&height=80')
        await self.bot.say(embed=emb)

    @commands.command(pass_context=True)
    async def help(self, ctx, *, cmd = None):
        """Shows this message."""
        author = ctx.message.author
        await self.bot.delete_message(ctx.message)
        pages = self.bot.formatter.format_help_for(ctx, self.bot)
        for page in pages:
            try:
                await self.bot.say(embed=page)
            except:
                await self.bot.say('I need the embed links perm.')




def setup(bot):
    bot.add_cog(Info(bot))
