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
        with open('data/options.json') as f:
            options = json.load(f)
            if 'CR_TAG' not in options:
                self.tag = None
            else:
                self.tag = options['CR_TAG']
        self.client = crasync.Client()
    

    @commands.command()
    async def profile(self, ctx, tag=None):
        '''Fetch a Clash Royale Profile!'''
        em = discord.Embed(title="Profile")
        em.color = await ctx.get_dominant_color(ctx.author.avatar_url)
        if tag is None and self.tag is None:
            em.description = "Please add `CR_TAG` to your options. Do `{p}options edit cr_tag <tag>`"
            return await ctx.send(embed=em)
        elif self.tag is not None:
            tag = self.tag

        tag = tag.strip('#').replace('O', '0')
        try:
            profile = await self.client.get_profile(tag)
        except:
            em.description = "Either API is down or that's an invalid tag."
            return await ctx.send(embed=em)
                                      
        em.title = profile.name
        em.set_thumbnail(url=profile.arena.image_url)
        em.description = f"#{tag}"
        em.url = f"http://cr-api.com/profile/{tag}"
        em.add_field(name='Current Trophies', value=profile.current_trophies)
        em.add_field(name='Highest Trophies', value=profile.highest_trophies)
        em.add_field(name='Legend Trophies', value=f'{profile.legend_trophies}')
        em.add_field(name='Level', value=profile.level)
        em.add_field(name='Experience', value=f"{profile.experience[0]}/{profile.experience[1]}")
        em.add_field(name='Wins/Losses/Draws', value=f'{profile.wins}/{profile.losses}/{profile.draws}')
        em.add_field(name='Global Rank', value=f'{profile.global_rank}')         
        em.add_field(name='Clan Info', value=f'{profile.clan_name}\n#{profile.clan_tag}\n{profile.clan_role}')
        em.add_field(name='Win Streak', value=f'{profile.win_streak}')
        em.set_footer(text="Powered By cr-api.com", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
        
        try:
            em.set_author(name="Profile", icon_url=profile.clan_badge_url)
        except:
            em.set_author(name='Profile')
        await ctx.send(embed=em) 


def setup(bot):
    bot.add_cog(ClashRoyale(bot))    
