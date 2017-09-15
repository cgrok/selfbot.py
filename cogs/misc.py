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
from ext.utility import parse_equation
from ext.colours import ColorNames
from sympy import solve
from PIL import Image
import asyncio
import random
import emoji
import copy
import io
import aiohttp

class Misc:
    def __init__(self, bot):
        self.bot = bot
        self.emoji_converter = commands.EmojiConverter()

    @commands.command()
    async def animate(self, ctx, *, file):
        '''Animate a text file on discord!'''
        try:
            with open(f'data/anims/{file}') as a:
                anim = a.read().splitlines()
        except:
            return await ctx.send('File not found.')
        interval = anim[0]
        base = await ctx.send(anim[1])
        for line in anim[2:]:
            await base.edit(content=line)
            await asyncio.sleep(float(interval))

    @commands.command()
    async def virus(self, ctx, virus=None, *, user : commands.MemberConverter=None):
        '''
        Destroy someone's device with this virus command!
        '''
        virus = virus or 'discord'
        user = user or ctx.author
        with open('data/virus.txt') as f:
            animation = f.read().splitlines()
        base = await ctx.send(animation[0])
        for line in animation[1:]:
            await base.edit(content=line.format(virus=virus, user=user))
            await asyncio.sleep(random.randint(1, 4))

    @commands.command()
    async def react(self, ctx, index : int, *, reactions):
        '''React to a specified message with reactions'''
        history = await ctx.channel.history(limit=10).flatten()
        message = history[index]
        async for emoji in self.validate_emojis(ctx, reactions):
            await message.add_reaction(emoji)

    async def validate_emojis(self, ctx, reactions):
        '''
        Checks if an emoji is valid otherwise, 
        tries to convert it into a custom emoji
        '''
        for emote in reactions.split():
            if emote in emoji.UNICODE_EMOJI:
                yield emote
            else:
                try:
                    yield await self.emoji_converter.convert(ctx, emote)
                except commands.BadArgument:
                    pass

    @commands.command(aliases=['color', 'colour', 'sc'])
    async def show_color(self, ctx, *, color : commands.ColourConverter):
        '''Enter a color and you will see it!'''
        file = io.BytesIO()
        Image.new('RGB', (200, 90), color.to_rgb()).save(file, format='PNG')
        file.seek(0)
        em = discord.Embed(color=color, title=f'Showing Color: {str(color)}')
        em.set_image(url='attachment://color.png')
        await ctx.send(file=discord.File(file, 'color.png'), embed=em)

    @commands.command(aliases=['dc','dominant_color'])
    async def dcolor(self, ctx, *, url):
        '''Fun command that shows the dominant color of an image'''
        await ctx.message.delete()
        color = await ctx.get_dominant_color(url)
        string_col = ColorNames.color_name(str(color))
        info = f'`{str(color)}`\n`{color.to_rgb()}`\n`{str(string_col)}`'
        em = discord.Embed(color=color, title='Dominant Color', description=info)
        em.set_thumbnail(url=url)
        file = io.BytesIO()
        Image.new('RGB', (200, 90), color.to_rgb()).save(file, format='PNG')
        file.seek(0)
        em.set_image(url="attachment://color.png")
        await ctx.send(file=discord.File(file, 'color.png'), embed=em)

    @commands.command()
    async def add(self, ctx, *numbers : int):
        '''Add multiple numbers together'''
        await ctx.send(f'Result: `{sum(numbers)}`')

    @commands.command()
    async def algebra(self, ctx, *, equation):
        '''Solve algabraic equations'''
        eq = parse_equation(equation)
        result = solve(eq)
        em = discord.Embed(
            color=discord.Color.green(),
            title='Equation', 
            description=f'```py\n{equation} = 0```',
            )
        em.add_field(name='Result', value=f'```py\n{result}```')
        await ctx.send(embed=em)

    @commands.group(invoke_without_command=True)
    async def emote(self, ctx, *, emoji : commands.EmojiConverter):
        '''Use emojis without nitro!'''
        await ctx.message.delete()
        async with ctx.session.get(emoji.url) as resp:
            image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, 'emoji.png'))

    @emote.command()
    async def copy(self, ctx, *, emoji : commands.EmojiConverter):
        '''Copy an emoji from another server to your own'''
        em = discord.Embed(color=discord.Color.green(), title=f'Added Emote: {emoji.name}')
        em.set_image(url='attachment://emoji.png')
        async with ctx.session.get(emoji.url) as resp:
            image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(embed=em, file=discord.File(copy.deepcopy(file), 'emoji.png'))
            await ctx.guild.create_custom_emoji(name=emoji.name, image=file.read())
    
    @commands.command()
    async def urban(self, ctx, *, search_terms : str):
        '''Searches Up a Term in Urban Dictionary'''
        search_terms = search_terms.split(" ")
        definition_number=terms=None
        try:
            definition_number = int(search_terms[-1]) - 1
            search_terms.remove(search_terms[-1])
        except ValueError:
            definition_number = 0
        if definition_number not in range(0, 11):
            pos = 0
        search_terms = "+".join(search_terms)
        url = "http://api.urbandictionary.com/v0/define?term=" + search_terms
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                result = await r.json()
        emb = discord.Embed()
        emb.color = await ctx.get_dominant_color(url=ctx.message.author.avatar_url)
        if result["list"]:
            definition = result['list'][definition_number]['definition']
            example = result['list'][definition_number]['example']
            defs = len(result['list'])
            search_terms = search_terms.split("+")
            emb.description = "{}\n\n**Example:\n**{}".format(definition, example)
            emb.title = "{}  ({}/{})".format(" ".join(search_terms), definition_number+1, defs)
        else:
            emb.title = "Search term not found."
        await ctx.send(embed=emb)    

def setup(bot):
	bot.add_cog(Misc(bot))