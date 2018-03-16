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

from __future__ import division
import discord
import math
import operator
import colorthief
import asyncio
import random
import emoji
import copy
import io
import aiohttp
import json
import os
import requests
import urllib.parse
import urbanasync
from discord.ext import commands
from ext.utility import parse_equation
from ext.colours import ColorNames
from urllib.request import urlopen
from bs4 import BeautifulSoup
from sympy import solve
from PIL import Image
from datetime import datetime
from discord.ext import commands
from pyparsing import (Literal,CaselessLiteral,Word,Combine,Group,Optional,
                    ZeroOrMore,Forward,nums,alphas,oneOf)
from discord.ext import commands
from ext.utility import parse_equation
from ext.colours import ColorNames
from urllib.request import urlopen
from sympy import solve
from PIL import Image
import safygiphy
from ext import embedtobox


class NumericStringParserForPython3(object):
    '''
    Most of this code comes from the fourFn.py pyparsing example

    '''
    def pushFirst(self, strg, loc, toks ):
        self.exprStack.append( toks[0] )
    def pushUMinus(self, strg, loc, toks ):
        if toks and toks[0]=='-':
            self.exprStack.append( 'unary -' )
    def __init__(self):
        """
        Please use any of the following symbols:
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        """
        point = Literal( "." )
        e     = CaselessLiteral( "E" )
        fnumber = Combine( Word( "+-"+nums, nums ) +
                        Optional( point + Optional( Word( nums ) ) ) +
                        Optional( e + Word( "+-"+nums, nums ) ) )
        ident = Word(alphas, alphas+nums+"_$")
        plus  = Literal( "+" )
        minus = Literal( "-" )
        mult  = Literal( "*" )
        div   = Literal( "/" )
        lpar  = Literal( "(" ).suppress()
        rpar  = Literal( ")" ).suppress()
        addop  = plus | minus
        multop = mult | div
        expop = Literal( "^" )
        pi    = CaselessLiteral( "PI" )
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                (pi|e|fnumber|ident+lpar+expr+rpar).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar+expr+rpar)
                ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + ZeroOrMore( ( expop + factor ).setParseAction( self.pushFirst ) )
        term = factor + ZeroOrMore( ( multop + factor ).setParseAction( self.pushFirst ) )
        expr << term + ZeroOrMore( ( addop + term ).setParseAction( self.pushFirst ) )
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = expr
        # this will map operator symbols to their corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {
                "+" : operator.add,
                "-" : operator.sub,
                "*" : operator.mul,
                "/" : operator.truediv,
                "^" : operator.pow }
        self.fn  = {
                "sin" : math.sin,
                "cos" : math.cos,
                "tan" : math.tan,
                "abs" : abs,
                "trunc" : lambda a: int(a),
                "round" : round,
                "sgn" : lambda a: abs(a)>epsilon and cmp(a,0) or 0}
    def evaluateStack(self, s ):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack( s )
        if op in "+-*/^":
            op2 = self.evaluateStack( s )
            op1 = self.evaluateStack( s )
            return self.opn[op]( op1, op2 )
        elif op == "PI":
            return math.pi # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op]( self.evaluateStack( s ) )
        elif op[0].isalpha():
            return 0
        else:
            return float( op )
    def eval(self,num_string,parseAll=True):
        self.exprStack=[]
        results=self.bnf.parseString(num_string,parseAll)
        val=self.evaluateStack( self.exprStack[:] )
        return val

class Misc:
    def __init__(self, bot):
        self.bot = bot
        self.emoji_converter = commands.EmojiConverter()
        self.nsp=NumericStringParserForPython3()
        
    @commands.command()
    async def gif(self, ctx, *, tag):
        ''' Get a random gif. Usage: gif <tag> 
        this command is sfw, to use nsfw gifs
        load community.nsfw '''
        g = safygiphy.Giphy()
        tag = tag.lower()
        with open('data/nsfw.json')as f:
            nsfwgif = json.load(f)
        if tag in nsfwgif:
            return await ctx.send('`Please use the nsfw commands to see content like this.`', delete_after=5)
        gif = g.random(tag=tag)
        color = await ctx.get_dominant_color(ctx.author.avatar_url)
        em = discord.Embed(color=color)
        em.set_image(url=str(gif.get('data', {}).get('image_original_url')))
        try:
            await ctx.send(embed=em)
        except discord.HTTPException:
            em_list = await embedtobox.etb(em)
            for page in em_list:
                await ctx.send(page)

    @commands.command()
    async def embedsay(self, ctx, *, message):
        '''Quick command to embed messages quickly.'''
        await ctx.message.delete()
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = message
        await ctx.send(embed=em)

    def prepare_code(self, code):
        def map_left_bracket(b, p):
            return (b, find_bracket(code, p + 1, b))

        def map_right_bracket(b, p):
            offset = find_bracket(list(reversed(code[:p])), 0, ']')
            return (b, p - offset)

        def map_bracket(b, p):
            if b == '[':
                return map_left_bracket(b, p)
            else:
                return map_right_bracket(b, p)

        return [map_bracket(c, i) if c in ('[', ']') else c
                for c, i in zip(code, range(len(code)))]

    def read(self, string):
        valid = ['>', '<', '+', '-', '.', ',', '[', ']']
        return self.prepare_code([c for c in string if c in valid])

    def eval_step(self, code, data, code_pos, data_pos):
        c = code[code_pos]
        d = data[data_pos]
        step = 1
        output = None

        if c == '>':
            data_pos = data_pos + 1
            if data_pos > len(data):
                data_pos = 0
        elif c == '<':
            if data_pos != 0:
                data_pos -= 1
        elif c == '+':
            if d == 255:
                data[data_pos] = 0
            else:
                data[data_pos] += 1
        elif c == '-':
            if d == 0:
                data[data_pos] = 255
            else:
                data[data_pos] -= 1
        elif c == '.':
            output = (chr(d))
        elif c == ',':
            data[data_pos] = ord(stdin.read(1))
        else:
            bracket, jmp = c
            if bracket == '[' and d == 0:
                step = 0
                code_pos = jmp
            elif bracket == ']' and d != 0:
                step = 0
                code_pos = jmp

        return (data, code_pos, data_pos, step, output)

    def bfeval(code, data=[0 for i in range(9999)], c_pos=0, d_pos=0):
        outputty = None
        while c_pos < len(code):
            out = None
            (data, c_pos, d_pos, step, output) = self.eval_step(code, data, c_pos, d_pos)
            if outputty == None and output == None:
                c_pos += step
            elif outputty == None and out == None and output != None:
                outputty = ''
                out = ''
                out = out + output
                outputty = outputty + out
                c_pos += step
            elif out == None and output != None:
                out = ''
                out = out + output
                outputty = outputty + out
                c_pos += step
            else:
                c_pos += step
        return outputty

    @commands.command()
    async def bf(self, ctx, slurp:str):
        '''Evaluate 'brainfuck' code (a retarded language).'''
        thruput = ctx.message.content
        preinput = thruput[5:]
        preinput2 = "\"\"\"\n" + preinput
        input = preinput2 + "\n\"\"\""
        code = self.read(input)
        output = self.bfeval(code)
        await ctx.send("Input:\n`{}`\nOutput:\n`{}`".format(preinput, output))

    @commands.command()
    async def py(self, ctx, *, code):
        '''Quick command to edit into a codeblock.'''
        await ctx.message.edit(content=f'```py\n{code}\n```')

    @commands.group(invoke_without_command=True, aliases=['anim'])
    async def animate(self, ctx, *, file):
        '''Animate a text file on discord!'''
        try:
            with open(f'data/anims/{file}.txt') as a:
                anim = a.read().splitlines()
        except:
            return await ctx.send('File not found.')
        interval = anim[0]
        for line in anim[1:]:
            await ctx.message.edit(content=line)
            await asyncio.sleep(float(interval))

    @animate.command()
    async def list(self, ctx):
        '''Lists all possible animations'''
        await ctx.send(f"Available animations: `{', '.join([f[:-4] for f in os.listdir('data/anims') if f.endswith('.txt')])}`")

    @commands.command()
    async def virus(self, ctx, virus=None, *, user: discord.Member = None):
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
    async def react(self, ctx, index: int, *, reactions):
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
    async def show_color(self, ctx, *, color: discord.Colour):
        '''Enter a color and you will see it!'''
        file = io.BytesIO()
        Image.new('RGB', (200, 90), color.to_rgb()).save(file, format='PNG')
        file.seek(0)
        em = discord.Embed(color=color, title=f'Showing Color: {str(color)}')
        em.set_image(url='attachment://color.png')
        await ctx.send(file=discord.File(file, 'color.png'), embed=em)

    @commands.command(aliases=['dc', 'dominant_color'])
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

    @commands.command(description='This command might get you banned')
    async def annoy(self, ctx, member: discord.Member=None, number: int=5):
        """ Usage: annoy @b1nzy#1337 50
        NOTICE: If you get banned, don't come back crying! """
        if number > 5:
            number = 5
        member = member or ctx.author
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        if member != None:
            for x in range(number):
                await ctx.channel.trigger_typing()
                await ctx.send(member.mention)
                await asyncio.sleep(8)
        else:
            return await ctx.send(f"{ctx.author.mention}, I don't know how to use commands. Help!")

    @commands.command()
    async def tinyurl(self, ctx, *, link: str):
        await ctx.message.delete()
        url = 'http://tinyurl.com/api-create.php?url=' + link
        async with ctx.session.get(url) as resp:
            new = await resp.text()
        emb = discord.Embed(colour=await ctx.get_dominant_color(ctx.author.avatar_url))
        emb.add_field(name="Original Link", value=link, inline=False)
        emb.add_field(name="Shortened Link", value=new, inline=False)
        await ctx.send(embed=emb)

    @commands.command(aliases=['calc', 'maths'])
    async def calculate(self, ctx, *, formula=None):
        """
        Do some real math
        finally a working command for mathematics
        thanks to Paul McGuire's fourFn.py module
        """
        person = ctx.message.author
        user = ctx.author

        if formula == None:
            # How can it calculate an empty message? Reee!
            msg = f'\u200BUsage: `{ctx.prefix}{ctx.invoked_with} [any maths formula]`'
            e = discord.Embed()
            e.color = await ctx.get_dominant_color(user.avatar_url)
            e.description = f'{msg}'
            await ctx.send(embed=e)
            return

        try:
            answer=self.nsp.eval(formula)
        except:
            # If there's a problem in the input, show examples
            msg = f'\N{THINKING FACE} wrong {formula} input.\nTry any of these:'
            e = discord.Embed()
            e.color = await ctx.get_dominant_color(user.avatar_url)
            e.description = f'\u200B{msg}'
            e.add_field(name='multiplication', value="`num` * `num`", inline=True)
            e.add_field(name='division', value="`num` / `num`", inline=True)
            e.add_field(name='addition', value="`num` + `num`", inline=True)
            e.add_field(name='rest', value="`num` - `num`", inline=True)
            e.add_field(name='exponential', value="`num` ^ `num`")
            e.add_field(name='integer', 
                        value="[`num` + `num` | `num` - `num`] `num` 0 `num`..`num` 9 `num` +")
            await ctx.send(embed=e, delete_after=60)
            return

        # Correct input prints correct answer
        e = discord.Embed()
        e.color = await ctx.get_dominant_color(user.avatar_url)
        e.add_field(name='Input:', value=f'```{formula}```', inline=True)
        e.add_field(name='Result:', value=f'```{round(answer, 2)}```', inline=True)
        await ctx.send(embed=e)

    @commands.command()
    async def algebra(self, ctx, *, equation):
        '''Solve algabraic equations'''
        eq = parse_equation(equation)
        result = solve(eq)
        em = discord.Embed()
        em.color = discord.Color.green()
        em.title = 'Equation'
        em.description = f'```py\n{equation} = 0```'
        em.add_field(name='Result', value=f'```py\n{result}```')
        await ctx.send(embed=em)

    def check_emojis(self, bot_emojis, emoji):
        for exist_emoji in bot_emojis:
            if emoji[0] == "<" or emoji[0] == "":
                if exist_emoji.name.lower() == emoji[1]:
                    return [True, exist_emoji]
            else:
                if exist_emoji.name.lower() == emoji[0]:
                    return [True, exist_emoji]
        return [False, None]

    @commands.group(invoke_without_command=True, name='emoji', aliases=['emote', 'e'])
    async def _emoji(self, ctx, *, emoji: str):
        '''Use emojis without nitro!'''
        emoji = emoji.split(":")
        emoji_check = self.check_emojis(ctx.bot.emojis, emoji)
        if emoji_check[0]:
            emo = emoji_check[1]
        else:
            emoji = [e.lower() for e in emoji]
            if emoji[0] == "<" or emoji[0] == "":
                emo = discord.utils.find(lambda e: emoji[1] in e.name.lower(), ctx.bot.emojis)
            else:
                emo = discord.utils.find(lambda e: emoji[0] in e.name.lower(), ctx.bot.emojis)
            if emo == None:
                em = discord.Embed(title="Send Emoji", description="Could not find emoji.")
                em.color = await ctx.get_dominant_color(ctx.author.avatar_url)
                await ctx.send(embed=em)
                return
        await ctx.send(str(emo))

    @_emoji.command()
    @commands.has_permissions(manage_emojis=True)
    async def copy(self, ctx, *, emoji: str):
        '''Copy an emoji from another server to your own'''
        if len(ctx.message.guild.emojis) == 50:
            await ctx.message.delete()
            await ctx.send('Your Server has already hit the 50 Emoji Limit!')
            return
        emo_check = self.check_emojis(ctx.bot.emojis, emoji.split(":"))
        if emo_check[0]:
            emo = emo_check[1]
        else:
            emo = discord.utils.find(lambda e: emoji.replace(":", "") in e.name, ctx.bot.emojis)
        em = discord.Embed()
        em.color = await ctx.get_dominant_color(ctx.author.avatar_url)
        if emo == None:
            em.title = 'Add Emoji'
            em.description = 'Could not find emoji.'
            await ctx.send(embed=em)
            return
        em.title = f'Added Emoji: {emo.name}'
        em.set_image(url='attachment://emoji.png')
        async with ctx.session.get(emo.url) as resp:
            image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(embed=em, file=discord.File(copy.deepcopy(file), 'emoji.png'))
            await ctx.guild.create_custom_emoji(name=emo.name, image=file.read())

    @commands.command(aliases=['emotes'])
    async def emojis(self, ctx):
        '''Lists all emojis in a server'''
        emotes = '\n'.join(['{1} `:{0}:`'.format(e.name, str(e)) for e in ctx.message.guild.emojis])
        if len(emotes) > 2000:
            paginated_text = ctx.paginate(emotes)
            for page in paginated_text:
                if page == paginated_text[-1]:
                    await ctx.send(f'{page}')
                    break
                await ctx.send(f'{page}')
            # for page in pages:
            #     await ctx.send(page)
            # async with ctx.session.post("https://hastebin.com/documents", data=code) as resp:
            #     data = await resp.json()
            # await ctx.send(content=f"Here are all the emotes you have: <https://hastebin.com/{data['key']}.py>")

            #await ctx.send()
        else:
            await ctx.send(emotes)

    @commands.command()
    async def urban(self, ctx, *, search_terms: str):
        '''Searches Up a Term in Urban Dictionary'''
        client = urbanasync.Client(ctx.session)
        search_terms = search_terms.split()
        definition_number = terms = None
        try:
            definition_number = int(search_terms[-1]) - 1
            search_terms.remove(search_terms[-1])
        except ValueError:
            definition_number = 0
        if definition_number not in range(0, 11):
            pos = 0
        search_terms = " ".join(search_terms)
        emb = discord.Embed()
        try:
            term = await client.get_term(search_terms)
        except LookupError:
            emb.title = "Search term not found."
            return await ctx.send(embed=emb)
        emb.color = await ctx.get_dominant_color(url=ctx.message.author.avatar_url)
        definition = term.definitions[definition_number]
        emb.title = f"{definition.word}  ({definition_number+1}/{len(term.definitions)})"
        emb.description = definition.definition
        emb.url = definition.permalink
        emb.add_field(name='Example', value=definition.example)
        emb.add_field(name='Votes', value=f'{definition.upvotes}👍    {definition.downvotes}👎')
        emb.set_footer(text=f"Definition written by {definition.author}", icon_url="http://urbandictionary.com/favicon.ico")
        await ctx.send(embed=emb)

    @commands.group(invoke_without_command=True)
    async def lenny(self, ctx):
        """Lenny and tableflip group commands"""
        msg = 'Available: `{}lenny face`, `{}lenny shrug`, `{}lenny tableflip`, `{}lenny unflip`'
        await ctx.send(msg.format(ctx.prefix))

    @lenny.command()
    async def shrug(self, ctx):
        """Shrugs!"""
        await ctx.message.edit(content='¯\\\_(ツ)\_/¯')

    @lenny.command()
    async def tableflip(self, ctx):
        """Tableflip!"""
        await ctx.message.edit(content='(╯°□°）╯︵ ┻━┻')

    @lenny.command()
    async def unflip(self, ctx):
        """Unfips!"""
        await ctx.message.edit(content='┬─┬﻿ ノ( ゜-゜ノ)')

    @lenny.command()
    async def face(self, ctx):
        """Lenny Face!"""
        await ctx.message.edit(content='( ͡° ͜ʖ ͡°)')

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question=None):
        """Ask questions to the 8ball"""
        with open('data/answers.json') as f:
            choices = json.load(f)
        author = ctx.message.author
        emb = discord.Embed()
        emb.color = await ctx.get_dominant_color(url=author.avatar_url)
        emb.set_author(name='\N{WHITE QUESTION MARK ORNAMENT} Your question:', icon_url=author.avatar_url)
        emb.description = question
        emb.add_field(name='\N{BILLIARDS} Your answer:', value=random.choice(choices), inline=True)
        await ctx.send(embed=emb)
    
    @commands.command()
    async def ascii(self, ctx, *, text):
        async with ctx.session.get(f"http://artii.herokuapp.com/make?text={urllib.parse.quote_plus(text)}") as f:
            message = await f.text()
        if len('```' + message + '```') > 2000:
            await ctx.send('Your ASCII is too long!')
            return
        await ctx.send('```' + message + '```')

    @commands.command()
    async def whoisplaying(self, ctx, *, game):
        message = ''
        for member in ctx.guild.members:
            if member.game != None:
                if member.game.name == game:
                    message += str(member) + '\n'
        await ctx.send(embed=discord.Embed(title=f'Who is playing {game}?', description = message, color=await ctx.get_dominant_color(url=ctx.message.author.avatar_url)))

    @commands.command()
    async def nickscan(self, ctx):
        message = '**Server | Nick**\n'
        for guild in self.bot.guilds:
            if guild.me.nick != None:
                message += f'{guild.name} | {guild.me.nick}\n'

        await ctx.send(embed=discord.Embed(title=f'Servers I Have Nicknames In', description = message, color=await ctx.get_dominant_color(url=ctx.message.author.avatar_url)))

    @commands.command()
    async def textmojify(self, ctx, *, msg):
        """Convert text into emojis"""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        if msg != None:
            out = msg.lower()
            text = out.replace(' ', '    ').replace('10', '\u200B:keycap_ten:')\
                      .replace('ab', '\u200B🆎').replace('cl', '\u200B🆑')\
                      .replace('0', '\u200B:zero:').replace('1', '\u200B:one:')\
                      .replace('2', '\u200B:two:').replace('3', '\u200B:three:')\
                      .replace('4', '\u200B:four:').replace('5', '\u200B:five:')\
                      .replace('6', '\u200B:six:').replace('7', '\u200B:seven:')\
                      .replace('8', '\u200B:eight:').replace('9', '\u200B:nine:')\
                      .replace('!', '\u200B❗').replace('?', '\u200B❓')\
                      .replace('vs', '\u200B🆚').replace('.', '\u200B🔸')\
                      .replace(',', '🔻').replace('a', '\u200B🅰')\
                      .replace('b', '\u200B🅱').replace('c', '\u200B🇨')\
                      .replace('d', '\u200B🇩').replace('e', '\u200B🇪')\
                      .replace('f', '\u200B🇫').replace('g', '\u200B🇬')\
                      .replace('h', '\u200B🇭').replace('i', '\u200B🇮')\
                      .replace('j', '\u200B🇯').replace('k', '\u200B🇰')\
                      .replace('l', '\u200B🇱').replace('m', '\u200B🇲')\
                      .replace('n', '\u200B🇳').replace('ñ', '\u200B🇳')\
                      .replace('o', '\u200B🅾').replace('p', '\u200B🅿')\
                      .replace('q', '\u200B🇶').replace('r', '\u200B🇷')\
                      .replace('s', '\u200B🇸').replace('t', '\u200B🇹')\
                      .replace('u', '\u200B🇺').replace('v', '\u200B🇻')\
                      .replace('w', '\u200B🇼').replace('x', '\u200B🇽')\
                      .replace('y', '\u200B🇾').replace('z', '\u200B🇿')
            try:
                await ctx.send(text)
            except Exception as e:
                await ctx.send(f'```{e}```')
        else:
            await ctx.send('Write something, reee!', delete_after=3.0)

    @commands.command(aliases=['yt', 'vid', 'video'])
    async def youtube(self, ctx, *, search):
        """Search for videos on YouTube"""
        search = search.replace(' ', '+').lower()
        response = requests.get(f"https://www.youtube.com/results?search_query={search}").text
        result = BeautifulSoup(response, "lxml")
        dir_address = f"{result.find_all(attrs={'class': 'yt-uix-tile-link'})[0].get('href')}"
        output=f"**Top Result:**\nhttps://www.youtube.com{dir_address}"
        try:
            await ctx.send(output)
            await ctx.message.delete()
        except discord.Forbidden:
            pass

    @commands.command()
    async def spaceify(self, ctx, *, text):
        await asyncio.sleep(0.1)
        await ctx.message.edit(text.replace('', ' '))

def setup(bot):
    bot.add_cog(Misc(bot))
