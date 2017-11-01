'''
MIT License

Copyright (c) 2017 Grok

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
import asyncio
import aiohttp
import crasync
import os
import json

class ClashRoyale:

    def __init__(self, bot):
        self.bot = bot
        with open('data/config.json') as f:
            config = json.load(f)
            if 'CR_TAG' not in config:
                tag = None
            else:
                tag = config['CR_TAG']
        self.tag = os.environ.get('CR_TAG') or tag
        self.client = crasync.Client()


    @commands.command()
    async def profile(self, ctx, tag=None):
        '''Fetch a Clash Royale Profile!'''
        em = discord.Embed(title="Profile")
        em.color = await ctx.get_dominant_color(ctx.author.avatar_url)
        if tag == None:
            tag = self.tag
            if tag == None:
                em.description = "Please add `CR_TAG` to your config."
                return await ctx.send(embed=em)
        try:
            profile = await self.client.get_profile(tag)
        except:
            em.description = "Either API is down or that's an invalid tag."
            return await ctx.send(embed=em)

        em.title = profile.name
        em.description = f"#{tag}"
        em.url = f"http://cr-api.com/profile/{tag}"
        try:
            em.set_author(name="Profile", icon_url=profile.clan_badge_url)
        except:
            em.set_author(name='Profile')

        await ctx.send(embed=em) 


def setup(bot):
    bot.add_cog(ClashRoyale(bot))
