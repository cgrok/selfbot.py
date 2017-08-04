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
                asyncio.sleep(5)
                await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def ban(self, ctx, member : discord.Member):
            '''Ban someone from the server.'''
            try:
                await self.bot.ban(member)
                await self.bot.edit_message(ctx.message, 'Banned {} from the server.'.format(member))
            except:
                await self.bot.edit_message(ctx.message, 'You dont have the permission to ban members.')
                asyncio.sleep(5)
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
        	asyncio.sleep(5)
        	await self.bot.delete_message(ctx.message)


    def find_user(self, bans, member): 
            return [user for user in bans if user.id == member or user.name.lower() == member.lower()]

    async def _unban(self, ctx, server, user):
    	try:
    		await self.bot.unban(server, user)
    		await self.bot.edit_message(ctx.message, 'Unbanned {} from the server.'.format(user))
    	except:
    		await self.bot.edit_message(ctx.message, 'You dont have the permission to un-ban members.')
    		asyncio.sleep(5)
    		await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def unban(self, ctx, member : str):
        '''Unban someone using their user ID or name.'''
        server = ctx.message.server
        try:
            bans = await self.bot.get_bans(server)
        except:
            await self.bot.edit_message(ctx.message, 'You dont have the permission to see the bans.')
            asyncio.sleep(5)
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
    		asyncio.sleep(5)
    		await self.bot.delete_message(ctx.message)
    	else:
    		await self.bot.edit_message(ctx.message,'**List of banned users:**```bf\n{}```'.format(', '.join([str(u) for u in bans])))

        


def setup(bot):
        bot.add_cog(Moderation(bot))
