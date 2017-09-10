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
import io
from PIL import Image

class Misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, *, msg):
        '''Say something as yourself! Wow!'''
        await ctx.send(msg)

    @commands.command()
    async def dominant_color(self, ctx, *, url):
        '''Fun command that shows the dominant color of an image'''
        await ctx.message.delete()
        color = await ctx.get_dominant_color(url)
        em = discord.Embed(color=color, title='Original Image', url=url)
        em.set_thumbnail(url=url)
        file = io.BytesIO()
        Image.new('RGB', (200, 200), color.to_rgb()).save(file, format='PNG')
        file.seek(0)
        await ctx.send(f'Showing color: `{str(color)}`', file=discord.File(file, 'color.png'), embed=em)


def setup(bot):
	bot.add_cog(Misc(bot))