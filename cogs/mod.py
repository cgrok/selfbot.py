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
import datetime
import time
import random
import asyncio
import json
import requests
import os

class Moderation:

    def __init__(self, bot):
            self.bot = bot


    @commands.command(pass_context=True)
    async def kick(self, ctx, member : discord.Member):
            '''Kick someone from the server.'''
            try:
                await self.bot.kick(member)
                await self.bot.edit_message(ctx.message, 'Kicked {} from the server.'.format(member))
            except:
                await self.bot.edit_message(ctx.message, 'You dont have the permission to kick members.')
                await asyncio.sleep(5)
                await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def ban(self, ctx, member : discord.Member):
            '''Ban someone from the server.'''
            try:
                await self.bot.ban(member)
                await self.bot.edit_message(ctx.message, 'Banned {} from the server.'.format(member))
            except:
                await self.bot.edit_message(ctx.message, 'You dont have the permission to ban members.')
                await asyncio.sleep(5)
                await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def softban(self,ctx, member : discord.Member):
        '''Kick someone out and delete their messages.'''
        try:
            await self.bot.ban(member)
            await self.bot.unban(member.server, member)
            await self.bot.edit_message(ctx.message, 'Soft-banned {}.'.format(member))
        except:
        	await self.bot.edit_message(ctx.message, 'You dont have the permission to ban members.')
        	await asyncio.sleep(5)
        	await self.bot.delete_message(ctx.message)


    def find_user(self, bans, member):
            return [user for user in bans if user.id == member or user.name.lower() == member.lower()]

    async def _unban(self, ctx, server, user):
    	try:
    		await self.bot.unban(server, user)
    		await self.bot.edit_message(ctx.message, 'Unbanned {} from the server.'.format(user))
    	except:
    		await self.bot.edit_message(ctx.message, 'You dont have the permission to un-ban members.')
    		await asyncio.sleep(5)
    		await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def unban(self, ctx, member : str):
        '''Unban someone using their user ID or name.'''
        server = ctx.message.server
        try:
            bans = await self.bot.get_bans(server)
        except:
            await self.bot.edit_message(ctx.message, 'You dont have the permission to see the bans.')
            await asyncio.sleep(5)
            await self.bot.delete_message(ctx.message)
            return

        users = self.find_user(bans, member)
        print(users)
        print([user.name for user in bans])

        if len(users) > 1:
        	return await self.bot.edit_message(ctx.message, 'Multiple users found.')
        if len(users) < 1:
        	return await self.bot.edit_message(ctx.message, 'User not found.')


        await self._unban(ctx, server, users[0])

    @commands.command(pass_context=True)
    async def bans(self, ctx):
    	'''See a list of banned users.'''
    	server = ctx.message.server
    	server = ctx.message.server
    	try:
    		bans = await self.bot.get_bans(server)
    	except:
    		await self.bot.edit_message(ctx.message, 'You dont have the permission to see the bans.')
    		await asyncio.sleep(5)
    		await self.bot.delete_message(ctx.message)
    	else:
    		await self.bot.edit_message(ctx.message,'**List of banned users:**```bf\n{}\n```'.format(', '.join([str(u) for u in bans])))

    @commands.command(aliases=['p'], pass_context=True)
    async def purge(self, ctx, msgs: int, *, txt=None):
        '''Purge messages if you have the perms.'''
        await self.bot.delete_message(ctx.message)
        if msgs < 10000:
            async for message in self.bot.logs_from(ctx.message.channel, limit=msgs):
                try:
                    if txt:
                        if txt.lower() in message.content.lower():
                            await self.bot.delete_message(message)
                    else:
                        await self.bot.delete_message(message)
                except:
                    pass
        else:
            await self.bot.send_message(ctx.message.channel, 'Too many messages to delete. Enter a number < 10000')


    @commands.command(aliases=['c'], pass_context=True)
    async def clean(self, ctx, msgs: int = 100):
        '''Shortcut to clean all your messages.'''
        await self.bot.delete_message(ctx.message)
        if msgs < 10000:
            async for message in self.bot.logs_from(ctx.message.channel, limit=msgs):
                try:
                    if message.author == self.bot.user:
                        await self.bot.delete_message(message)
                except:
                    pass
        else:
            await self.bot.send_message(ctx.message.channel, 'Too many messages to delete. Enter a number < 10000')

    @commands.command(pass_context=True)
    async def addrole(self, ctx, member: discord.Member, *, rolename: str):
        '''Add a role to someone else.'''
        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.server.roles)
        if not role:
            return await self.bot.say('That role does not exist.')
        try:
            await self.bot.add_roles(member, role)
            await self.bot.say("Added: `{}`".format(role.name))
        except:
            await self.bot.say("I dont have the perms to add that role.")

    @commands.command(pass_context=True)
    async def removerole(self, ctx, member: discord.Member, *, rolename: str):
        '''Remove a role from someone else.'''
        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.server.roles)
        if not role:
            return await self.bot.say('That role does not exist.')
        try:
            await self.bot.remove_roles(member, role)
            await self.bot.say("Removed: `{}`".format(role.name))
        except:
            await self.bot.say("I dont have the perms to add that role.")


    @commands.command(pass_context = True)
    async def warn(self, ctx, user: discord.Member=None, reason=None):
        '''Warn a member'''
        warning = 'You have been warned in **{}** by **{}** for: **{}**'
        server = ctx.message.server
        author = ctx.message.author
        await self.bot.say('**{}** has been warned'.format(user))
        await self.bot.send_message(user, warning.format(server, author, reason))
        await self.bot.delete_message(ctx.message)

        
    @commands.command(pass_context = True)
    @commands.has_permissions(manage_channels=True)
    async def muteall(self, ctx):
        '''Denies the @everyone role to send messages'''
        everyone_perms = ctx.message.channel.overwrites_for(ctx.message.server.default_role)
        everyone_perms.send_messages = False
        await self.bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.default_role, everyone_perms)
        await self.answer_done(ctx.message)
        

    @commands.command(pass_context = True)
    @commands.has_permissions(manage_channels=True)
    async def unmuteall(self, ctx):
        '''Allows the @everyone role to send messages'''
        everyone_perms = ctx.message.channel.overwrites_for(ctx.message.server.default_role)
        everyone_perms.send_messages = True
        await self.bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.default_role, everyone_perms)
        await self.answer_done(ctx.message)

    @commands.command(pass_context = True)
    @commands.has_permissions(manage_channels=True)
    async def mute(self, ctx, user: discord.Member):
        '''Denies someone from sending messages'''
        perms = ctx.message.channel.overwrites_for(user)
        perms.send_messages = False
        await self.bot.edit_channel_permissions(ctx.message.channel, user, perms)
        await self.answer_done(ctx.message)

    @commands.command(pass_context = True)
    @commands.has_permissions(manage_channels=True)
    async def unmute(self, ctx, user: discord.Member):
        '''Allows someone to send messages'''
        perms = ctx.message.channel.overwrites_for(user)
        perms.send_messages = None
        if not perms.is_empty():
                await self.bot.edit_channel_permissions(ctx.message.channel, user, perms)
        else:
                await self.bot.delete_channel_permissions(ctx.message.channel, user)
                await self.answer_done(ctx.message)

    @commands.command(pass_context = True)
    @commands.has_permissions(manage_channels=True)
    async def unblock(self, ctx, user: discord.Member):
        '''Allows someone to view a channel'''
        perms = ctx.message.channel.overwrites_for(user)
        perms.read_messages = None
        if not perms.is_empty():
                await self.bot.edit_channel_permissions(ctx.message.channel, user, perms)
        else:
                await self.bot.delete_channel_permissions(ctx.message.channel, user)
                await self.answer_done(ctx.message)

    @commands.command(pass_context = True)
    @commands.has_permissions(manage_channels=True)
    async def block(self, ctx, user: discord.Member):
        """Denies someone from viewing the channel"""
        perms = ctx.message.channel.overwrites_for(user)
        perms.read_messages = False
        await self.bot.edit_channel_permissions(ctx.message.channel, user, perms)
        await self.answer_done(ctx.message)

def setup(bot):
        bot.add_cog(Moderation(bot))
