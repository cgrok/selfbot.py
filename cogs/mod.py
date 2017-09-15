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
from urllib.parse import urlparse
import datetime
import asyncio
import random
import pip
import os
import io


class Mod:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member : commands.MemberConverter):
        '''Kick someone from the server.'''
        emb = discord.Embed(title='Kick')
        emb.color = await ctx.get_dominant_color(member.avatar_url)
        emb.set_thumbnail(url=member.avatar_url)
        await ctx.message.delete()
        try:
            emb.description = "{} was just kicked.".format(member)
            await ctx.guild.kick(member)
        except:
            emb.description = "You do not have the permissions to kick users."
        await ctx.send(embed=emb)

    @commands.command()
    async def ban(self, ctx, member : commands.MemberConverter):
        '''Ban someone from the server.'''
        emb = discord.Embed(title='Ban')
        emb.color = await ctx.get_dominant_color(member.avatar_url)
        emb.set_thumbnail(url=member.avatar_url)
        await ctx.message.delete()
        try:
            emb.description = "{} was just banned.".format(member)
            await ctx.guild.ban(member)
        except:
            emb.description = "You do not have the permissions to ban users."
        await ctx.send(embed=emb)

    @commands.command()
    async def purge(self, ctx, limit : int):
        '''Clean a number of messages'''
        await ctx.purge(limit) # TODO: add more functionality

    @commands.command()
    async def clean(self, ctx, limit : int=15):
        '''Clean a number of your own messages'''
        await ctx.purge(limit, lambda m: m.author == ctx.author)



def setup(bot):
	bot.add_cog(Mod(bot))
