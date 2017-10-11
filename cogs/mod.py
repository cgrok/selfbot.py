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

    async def format_mod_embed(self, ctx, user, success, method):
        '''Helper func to format an embed to prevent extra code'''
        emb = discord.Embed()
        emb.set_author(name=method.title(), icon_url=user.avatar_url)
        emb.color = await ctx.get_dominant_color(user.avatar_url)
        emb.set_footer(text=f'User ID: {user.id}')
        if success:
            if method == 'ban':
                emb.description = f'{user} was just {method}ned.'
            else:
                emb.description = f'{user} was just {method}ed.'
        else:
            emb.description = f"You do not have the permissions to {method} users."

        return emb

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason='Please write a reason!'):
        '''Kick someone from the server.'''
        try:
            await ctx.guild.kick(member, reason=reason)
        except:
            success = False
        else:
            success = True

        emb = await self.format_mod_embed(ctx, member, success, 'kick')

        await ctx.send(embed=emb)

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason='Please write a reason!'):
        '''Ban someone from the server.'''
        try:
            await ctx.guild.ban(member, reason=reason)
        except:
            success = False
        else:
            success = True

        emb = await self.format_mod_embed(ctx, member, success, 'ban')

        await ctx.send(embed=emb)

    @commands.command()
    async def unban(self, ctx, name_or_id, *, reason=None):
        '''Unban someone from the server.'''
        ban = await ctx.get_ban(name_or_id)

        try:
            await ctx.guild.unban(ban.user, reason=reason)
        except:
            success = False
        else:
            success = True
        
        emb = await self.format_mod_embed(ctx, ban.user, success, 'unban')

        await ctx.send(embed=emb)

    @commands.command(aliases=['del','p','prune'])
    async def purge(self, ctx, limit : int):
        '''Clean a number of messages'''
        await ctx.purge(limit=limit+1) # TODO: add more functionality

    @commands.command()
    async def clean(self, ctx, limit : int=15):
        '''Clean a number of your own messages'''
        await ctx.purge(limit=limit+1, check=lambda m: m.author == ctx.author)


    @commands.command()
    async def bans(self, ctx):
        '''See a list of banned users in the guild'''
        try:
            bans = await ctx.guild.bans()
        except:
            return await ctx.send('You dont have the perms to see bans.')

        em = discord.Embed(title=f'List of Banned Members ({len(bans)}):')
        em.description = ', '.join([str(b.user) for b in bans])
        em.color = await ctx.get_dominant_color(ctx.guild.icon_url)

        await ctx.send(embed=em)

    @commands.command()
    async def baninfo(self, ctx, *, name_or_id):
        '''Check the reason of a ban from the audit logs.'''
        ban = await ctx.get_ban(name_or_id)
        em = discord.Embed()
        em.color = await ctx.get_dominant_color(ban.user.avatar_url)
        em.set_author(name=str(ban.user), icon_url=ban.user.avatar_url)
        em.add_field(name='Reason', value=ban.reason or 'None')
        em.set_thumbnail(url=ban.user.avatar_url)
        em.set_footer(text=f'User ID: {ban.user.id}')

        await ctx.send(embed=em)

    @commands.command()
    async def addrole(self, ctx, member: discord.Member, *, rolename: str):
        '''Add a role to someone else.'''
        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
        if not role:
            return await ctx.send('That role does not exist.')
        try:
            await member.add_roles(role)
            await ctx.send(f'Added: `{role.name}`')
        except:
            await ctx.send("I don't have the perms to add that role.")


    @commands.command()
    async def removerole(self, ctx, member: discord.Member, *, rolename: str):
        '''Remove a role from someone else.'''
        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
        if not role:
            return await ctx.send('That role does not exist.')
        try:
            await member.remove_roles(role)
            await ctx.send(f'Removed: `{role.name}`')
        except:
            await ctx.send("I don't have the perms to add that role.")



def setup(bot):
	bot.add_cog(Mod(bot))
