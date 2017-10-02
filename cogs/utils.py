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
from discord.ext.commands import TextChannelConverter
from contextlib import redirect_stdout
from ext.utility import load_json
from urllib.parse import parse_qs
from mtranslate import translate
from lxml import etree
from ext import fuzzy
from ext import embedtobox
from PIL import Image
import unicodedata
import traceback
import textwrap
import wikipedia
import aiohttp
import inspect
import re
import io

class Utility:
    '''Useful commands to make your life easier'''
    def __init__(self, bot):
        self.bot = bot
        self.lang_conv = load_json('data/langs.json')
        self._last_embed = None
        self._rtfm_cache = None
        self._last_google = None
        self._last_result = None


    @commands.command(name='logout')
    async def _logout(self, ctx):
        '''
        Shuts down the selfbot,
        equivalent to a restart if you are hosting the bot on heroku.
        '''
        await ctx.send('`Selfbot Logging out...`')
        await self.bot.logout()

    @commands.command(name='help')
    async def new_help_command(self, ctx, *commands : str):
        """Shows this message."""
        destination = ctx.message.author if self.bot.pm_help else ctx.message.channel

        def repl(obj):
            return self.bot._mentions_transforms.get(obj.group(0), '')

        # help by itself just lists our own commands.
        if len(commands) == 0:
            pages = await self.bot.formatter.format_help_for(ctx, self.bot)
        elif len(commands) == 1:
            # try to see if it is a cog name
            name = self.bot._mention_pattern.sub(repl, commands[0])
            command = None
            if name in self.bot.cogs:
                command = self.bot.cogs[name]
            else:
                command = self.bot.all_commands.get(name)
                if command is None:
                    await destination.send(self.bot.command_not_found.format(name))
                    return

            pages = await self.bot.formatter.format_help_for(ctx, command)
        else:
            name = self.bot._mention_pattern.sub(repl, commands[0])
            command = self.bot.all_commands.get(name)
            if command is None:
                await destination.send(self.bot.command_not_found.format(name))
                return

            for key in commands[1:]:
                try:
                    key = self.bot._mention_pattern.sub(repl, key)
                    command = command.all_commands.get(key)
                    if command is None:
                        await destination.send(self.bot.command_not_found.format(key))
                        return
                except AttributeError:
                    await destination.send(self.bot.command_has_no_subcommands.format(command, key))
                    return

            pages = await self.bot.formatter.format_help_for(ctx, command)

        if self.bot.pm_help is None:
            characters = sum(map(lambda l: len(l), pages))
            # modify destination based on length of pages.
            if characters > 1000:
                destination = ctx.message.author

        color = await ctx.get_dominant_color(ctx.author.avatar_url)

        for embed in pages:
            embed.color = color
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException:
                em_list = await embedtobox.etb(embed)
                for page in em_list:
                    await ctx.send(page)

    @commands.command(name='presence')
    async def _presence(self, ctx, status, *, message=None):
        '''Change your Discord status! (Stream, Online, Idle, DND, Invisible, or clear it)'''
        status = status.lower()
        emb = discord.Embed(title="Presence")
        emb.color = await ctx.get_dominant_color(ctx.author.avatar_url)
        file = io.BytesIO()
        if status == "online":
            await self.bot.change_presence(status=discord.Status.online, game=discord.Game(name=message), afk=True)
            color = discord.Color(value=0x43b581).to_rgb()
        elif status == "idle":
            await self.bot.change_presence(status=discord.Status.idle, game=discord.Game(name=message), afk=True)
            color = discord.Color(value=0xfaa61a).to_rgb()
        elif status == "dnd":
            await self.bot.change_presence(status=discord.Status.dnd, game=discord.Game(name=message), afk=True)
            color = discord.Color(value=0xf04747).to_rgb()
        elif status == "invis" or status == "invisible":
            await self.bot.change_presence(status=discord.Status.invisible, game=discord.Game(name=message), afk=True)
            color = discord.Color(value=0x747f8d).to_rgb()
        elif status == "stream":
            await self.bot.change_presence(status=discord.Status.online, game=discord.Game(name=message,type=1,url=f'https://www.twitch.tv/{message}'), afk=True)
            color = discord.Color(value=0x593695).to_rgb()
        elif status == "clear":
            await self.bot.change_presence(game=None, afk=True)
            emb.description = "Presence cleared."
            return await ctx.send(embed=emb)
        else:
            emb.description = "Please enter either `online`, `idle`, `dnd`, `invisible`, or `clear`."
            return await ctx.send(embed=emb)

        Image.new('RGB', (500, 500), color).save(file, format='PNG')
        emb.description = "Your presence has been changed."
        file.seek(0)
        emb.set_author(name=status.title(), icon_url="attachment://color.png")
        try:
            await ctx.send(file=discord.File(file, 'color.png'), embed=emb)
        except discord.HTTPException:
            em_list = await embedtobox.etb(emb)
            for page in em_list:
                await ctx.send(page)


    @commands.command()
    async def source(self, ctx, *, command):
        '''See the source code for any command.'''
        source = str(inspect.getsource(self.bot.get_command(command).callback))
        fmt = '```py\n'+source.replace('`','\u200b`')+'\n```'
        if len(fmt) > 2000:
            async with ctx.session.post("https://hastebin.com/documents", data=source) as resp:
                data = await resp.json()
            key = data['key']
            return await ctx.send(f'Command source: <https://hastebin.com/{key}.py>')
        else:
            return await ctx.send(fmt)


    @commands.command()
    async def copy(self, ctx, id : int, channel : discord.TextChannel=None):
        '''Copy someones message by ID'''
        await ctx.message.delete()
        msg = await ctx.get_message(channel or ctx.channel, id)
        if len(msg.embeds) > 1:
            await ctx.send(msg.content, embed=msg.embeds[0])
            for embed in msg.embeds[1:]:
                await ctx.send(embed=embed)
        else:
            if msg.embeds:
                await ctx.send(msg.content, embed=msg.embeds[0])
            else:
                await ctx.send(msg.content)

    @commands.command()
    async def quote(self, ctx, id : int, channel : discord.TextChannel=None):
        """Quote someone's message by ID"""
        await ctx.message.delete()

        msg = await ctx.get_message(channel or ctx.channel, id)

        if not msg:
            return await ctx.send('Could not find that message!', delete_after=3.0)

        em = discord.Embed(color=0x00FFFF, description=msg.clean_content, timestamp=msg.created_at)
        em.set_author(name=str(msg.author), icon_url=msg.author.avatar_url)

        if isinstance(msg.channel, discord.TextChannel):
            em.set_footer(text='#'+str(msg.channel))
        else:
            em.set_footer(text=str(msg.channel))

        await ctx.send(embed=em)

    @commands.command()
    async def charinfo(self, ctx, *, characters: str):
        """Shows you information about a number of characters."""
        if len(characters) > 15:
            return await ctx.send('Too many characters ({}/15)'.format(len(characters)))

        fmt = '`\\U{0:>08}`: `\\N{{{1}}}` - `{2}` - <http://www.fileformat.info/info/unicode/char/{0}>'

        def to_string(c):
            digit = format(ord(c), 'x')
            name = unicodedata.name(c, 'Name not found.')
            return fmt.format(digit, name, c)

        await ctx.send('\n'.join(map(to_string, characters)))

    @commands.group()
    async def translate(self, ctx, lang, *, text):
        """Translate text!"""
        conv = self.lang_conv
        if lang in conv:
            return await self.bot.say('```{}```'.format(translate(text, lang)))
        lang = dict(zip(conv.values(), conv.keys())).get(lang.lower().title())
        if lang:
            await ctx.send('```{}```'.format(translate(text, lang)))
        else:
            await ctx.send('```That is not an available language.```')

    @translate.command()
    async def langs(self, ctx):
        '''Lists all available languages'''
        em = discord.Embed(color=discord.Color.blue(),
                           title='Available Languages',
                           description=', '.join(codes.values()))
        await ctx.send(embed=em)

    @commands.command(name='last_embed')
    async def _last_embed(self, ctx):
        '''Sends the command used to send the last embed'''
        await ctx.send('`'+self._last_embed+'`')

    @commands.command()
    async def embed(self, ctx, *, params):
        '''Send complex rich embeds with this command!'''
        em = self.to_embed(ctx, params)
        await ctx.message.delete()
        try:
            await ctx.send(embed=em)
            self._last_embed = params
        except:
            await ctx.send('Improperly formatted embed!')

    @commands.group(aliases=['rtfd'], invoke_without_command=True)
    async def rtfm(self, ctx, *, obj: str = None):
        """
        Gives you a documentation link for a discord.py entity.
        Written by Rapptz
        """
        await self.do_rtfm(ctx, 'rewrite', obj)

    @commands.command(pass_context=True)
    async def wiki(self, ctx, *, search: str = None):
        '''Addictive Wikipedia results'''
        if search == None:
            await ctx.channel.send(f'Usage: `{ctx.prefix}wiki [search terms]`')
            return

        results = wikipedia.search(search)
        if not len(results):
            no_results = await ctx.channel.send("Sorry, didn't find any result.")
            await asyncio.sleep(5)
            await ctx.message.delete(no_results)
            return

        newSearch = results[0]
        try:
            wik = wikipedia.page(newSearch)
        except wikipedia.DisambiguationError:
            more_details = await ctx.channel.send('Please input more details.')
            await asyncio.sleep(5)
            await ctx.message.delete(more_details)
            return

        emb = discord.Embed()
        emb.color = await ctx.get_dominant_color(url=ctx.message.author.avatar_url)
        emb.title = wik.title
        emb.url = wik.url
        textList = textwrap.wrap(wik.content, 500, break_long_words=True, replace_whitespace=False)
        emb.add_field(name="Wikipedia Results", value=textList[0] + "...")
        await ctx.message.edit(embed=emb)

    @commands.command(aliases=['g'])
    async def google(self ,ctx, *, query):
        """
        Searches google and gives you top result.
        Written By Rapptz
        """
        await ctx.trigger_typing()
        try:
            card, entries = await self.get_google_entries(ctx, query)
        except RuntimeError as e:
            await ctx.send(str(e))
        else:
            if card:
                value = '\n'.join(entries[:3])
                if value:
                    card.add_field(name='Search Results', value=value, inline=False)
                return await ctx.send(embed=card)

            if len(entries) == 0:
                return await ctx.send('No results found... sorry.')

            next_two = entries[1:3]
            first_entry = entries[0]
            if first_entry[-1] == ')':
                first_entry = first_entry[:-1] + '%29'

            if next_two:
                formatted = '\n'.join(map(lambda x: '<%s>' % x, next_two))
                msg = '{}\n\n**See also:**\n{}'.format(first_entry, formatted)
            else:
                msg = first_entry

            self._last_google = msg
            await ctx.send(msg)

    def to_embed(self, ctx, params):
        '''Actually formats the parsed parameters into an Embed'''
        em = discord.Embed()

        if not params.count('{'):
            if not params.count('}'):
                em.description = params

        for field in self.get_parts(params):
            data = self.parse_field(field)

            color = data.get('color') or data.get('colour')
            if color:
                color = int(color.strip('#'), 16)
                em.color = discord.Color(color)

            if data.get('description'):
                em.description = data['description']

            if data.get('title'):
                em.title = data['title']

            if data.get('url'):
                em.url = data['url']

            author = data.get('author')
            icon, url = data.get('icon'), data.get('url')

            if author:
                em._author = {'name': author}
                if icon:
                    em._author['icon_url'] = icon
                if url:
                    em._author['url'] = url

            field, value = data.get('field'), data.get('value')
            inline = False if str(data.get('inline')).lower() == 'false' else True
            if field and value:
                em.add_field(name=field, value=value, inline=inline)

            if data.get('thumbnail'):
                em._thumbnail = {'url': data['thumbnail']}

            if data.get('image'):
                em._image = {'url': data['image']}

            if data.get('footer'):
                em._footer = {'text': data.get('footer')}
                if data.get('icon'):
                    em._footer['icon_url'] = data.get('icon')

            if 'timestamp' in data.keys() and len(data.keys()) == 1:
                em.timestamp = ctx.message.created_at

        return em

    def get_parts(self, string):
        '''
        Splits the sections of the embed command
        '''
        for i, char in enumerate(string):
            if char == "{":
                ret = ""
                while char != "}":
                    i += 1
                    char = string[i]
                    ret += char
                yield ret.rstrip('}')

    def parse_field(self, string):
        '''
        Recursive function to get all the key val
        pairs in each section of the parsed embed command
        '''
        ret = {}

        parts = string.split(':')
        key = parts[0].strip().lower()
        val = ':'.join(parts[1:]).strip()

        ret[key] = val

        if '|' in string:
            string = string.split('|')
            for part in string:
                ret.update(self.parse_field(part))
        return ret

    async def build_rtfm_lookup_table(self):
        cache = {}

        page_types = {
            'rewrite': (
                'http://discordpy.rtfd.io/en/rewrite/api.html',
                'http://discordpy.rtfd.io/en/rewrite/ext/commands/api.html'
            )
        }

        for key, pages in page_types.items():
            sub = cache[key] = {}
            for page in pages:
                async with self.bot.session.get(page) as resp:
                    if resp.status != 200:
                        raise RuntimeError('Cannot build rtfm lookup table, try again later.')

                    text = await resp.text(encoding='utf-8')
                    root = etree.fromstring(text, etree.HTMLParser())
                    if root is not None:
                        nodes = root.findall(".//dt/a[@class='headerlink']")
                        for node in nodes:
                            href = node.get('href', '')
                            as_key = href.replace('#discord.', '').replace('ext.commands.', '')
                            sub[as_key] = page + href

        self._rtfm_cache = cache

    async def do_rtfm(self, ctx, key, obj):
        base_url = 'http://discordpy.rtfd.io/en/{}/'.format(key)

        if obj is None:
            await ctx.send(base_url)
            return

        if not self._rtfm_cache:
            await ctx.trigger_typing()
            await self.build_rtfm_lookup_table()

        # identifiers don't have spaces
        obj = obj.replace(' ', '_')

        if key == 'rewrite':
            pit_of_success_helpers = {
                'vc': 'VoiceClient',
                'msg': 'Message',
                'color': 'Colour',
                'perm': 'Permissions',
                'channel': 'TextChannel',
                'chan': 'TextChannel',
            }

            # point the abc.Messageable types properly:
            q = obj.lower()
            for name in dir(discord.abc.Messageable):
                if name[0] == '_':
                    continue
                if q == name:
                    obj = 'abc.Messageable.{}'.format(name)
                    break

            def replace(o):
                return pit_of_success_helpers.get(o.group(0), '')

            pattern = re.compile('|'.join(r'\b{}\b'.format(k) for k in pit_of_success_helpers.keys()))
            obj = pattern.sub(replace, obj)

        cache = self._rtfm_cache[key]
        matches = fuzzy.extract_or_exact(obj, cache, scorer=fuzzy.token_sort_ratio, limit=5, score_cutoff=50)

        e = discord.Embed(colour=discord.Colour.blurple())
        if len(matches) == 0:
            return await ctx.send('Could not find anything. Sorry.')

        e.description = '\n'.join('[{}]({}) ({}%)'.format(key, url, p) for key, p, url in matches)
        await ctx.send(embed=e)

    def parse_google_card(self, node):
        if node is None:
            return None

        e = discord.Embed(colour=0x00FFFF)

        # check if it's a calculator card:
        calculator = node.find(".//table/tr/td/span[@class='nobr']/h2[@class='r']")
        if calculator is not None:
            e.title = 'Calculator'
            e.description = ''.join(calculator.itertext())
            return e

        parent = node.getparent()

        # check for unit conversion card
        unit = parent.find(".//ol//div[@class='_Tsb']")
        if unit is not None:
            e.title = 'Unit Conversion'
            e.description = ''.join(''.join(n.itertext()) for n in unit)
            return e

        # check for currency conversion card
        currency = parent.find(".//ol/table[@class='std _tLi']/tr/td/h2")
        if currency is not None:
            e.title = 'Currency Conversion'
            e.description = ''.join(currency.itertext())
            return e

        # check for release date card
        release = parent.find(".//div[@id='_vBb']")
        if release is not None:
            try:
                e.description = ''.join(release[0].itertext()).strip()
                e.title = ''.join(release[1].itertext()).strip()
                return e
            except:
                return None

        # check for definition card
        words = parent.find(".//ol/div[@class='g']/div/h3[@class='r']/div")
        if words is not None:
            try:
                definition_info = words.getparent().getparent()[1] # yikes
            except:
                pass
            else:
                try:
                    e.title = words[0].text
                    e.description = words[1].text
                except:
                    return None

                for row in definition_info:
                    if len(row.attrib) != 0:
                        break
                    try:
                        data = row[0]
                        lexical_category = data[0].text
                        body = []
                        for index, definition in enumerate(data[1], 1):
                            body.append('%s. %s' % (index, definition.text))

                        e.add_field(name=lexical_category, value='\n'.join(body), inline=False)
                    except:
                        continue

                return e

        # check for "time in" card
        time_in = parent.find(".//ol//div[@class='_Tsb _HOb _Qeb']")
        if time_in is not None:
            try:
                time_place = ''.join(time_in.find("span[@class='_HOb _Qeb']").itertext()).strip()
                the_time = ''.join(time_in.find("div[@class='_rkc _Peb']").itertext()).strip()
                the_date = ''.join(time_in.find("div[@class='_HOb _Qeb']").itertext()).strip()
            except:
                return None
            else:
                e.title = time_place
                e.description = '%s\n%s' % (the_time, the_date)
                return e

        weather = parent.find(".//ol//div[@class='e']")
        if weather is None:
            return None

        location = weather.find('h3')
        if location is None:
            return None

        e.title = ''.join(location.itertext())

        table = weather.find('table')
        if table is None:
            return None

        try:
            tr = table[0]
            img = tr[0].find('img')
            category = img.get('alt')
            image = 'https:' + img.get('src')
            temperature = tr[1].xpath("./span[@class='wob_t']//text()")[0]
        except:
            return None # RIP
        else:
            e.set_thumbnail(url=image)
            e.description = '*%s*' % category
            e.add_field(name='Temperature', value=temperature)

        # On the 4th column it tells us our wind speeds
        try:
            wind = ''.join(table[3].itertext()).replace('Wind: ', '')
        except:
            return None
        else:
            e.add_field(name='Wind', value=wind)

        # On the 5th column it tells us our humidity
        try:
            humidity = ''.join(table[4][0].itertext()).replace('Humidity: ', '')
        except:
            return None
        else:
            e.add_field(name='Humidity', value=humidity)

        return e

    async def get_google_entries(self, ctx, query):
        params = {
            'q': query,
            'safe': 'on',
            'lr': 'lang_en',
            'hl': 'en'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
        }

        # list of URLs
        entries = []

        # the result of a google card, an embed
        card = None

        async with ctx.session.get('https://www.google.com/search', params=params, headers=headers) as resp:
            if resp.status != 200:
                raise RuntimeError('Google somehow failed to respond.')

            root = etree.fromstring(await resp.text(), etree.HTMLParser())

            card_node = root.find(".//div[@id='topstuff']")
            card = self.parse_google_card(card_node)

            search_nodes = root.findall(".//div[@class='g']")
            for node in search_nodes:
                url_node = node.find('.//h3/a')
                if url_node is None:
                    continue

                url = url_node.attrib['href']
                if not url.startswith('/url?'):
                    continue

                url = parse_qs(url[5:])['q'][0]

                entries.append(url)

        return card, entries


    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        await self.edit_to_codeblock(ctx, body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await err.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if self.bot.token in value:
                value = value.replace(self.bot.token,"[EXPUNGED]")
            if ret is None:
                if value:
                    try:
                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = ctx.paginate(f"{value}")
                        for page in paginated_text:
                            out = await ctx.send(f'```py{page}```')
            else:
                self._last_result = ret
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = ctx.paginate(f"{value}{ret}")
                    for page in paginated_text:
                        out = await ctx.send(f'```py\n{page}\n```')

        if out:
            await out.add_reaction('\u2705')
        if err:
            await err.add_reaction('\u2049')


    async def edit_to_codeblock(self, ctx, body):
        msg = f'```py\n{body}\n```'
        await ctx.message.edit(content=msg)


    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

def setup(bot):
    bot.add_cog(Utility(bot))
