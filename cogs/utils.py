import discord
from discord.ext import commands


class Utility:
    def __init__(self, bot):
        self.bot = bot
        self.last_embed = None

    @commands.command(name='last_embed')
    async def _last_embed(self, ctx):
        '''Sends the command used to send the last embed'''
        await ctx.send('`'+self.last_embed+'`')

    @commands.command()
    async def embed(self, ctx, *, params):
        '''Send complex rich embeds with this command!'''
        em = self.to_embed(ctx, params)
        await ctx.message.delete()
        try:
            await ctx.send(embed=em)
            self.last_embed = params
        except:
            await ctx.send('Improperly formatted embed!')

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
        '''Splits the parts of the embed'''
        for i, char in enumerate(string):
            if char == "{":
                ret = ""
                while char != "}":
                    i += 1
                    char = string[i]
                    ret += char
                yield ret.rstrip('}')
                    

    def parse_field(self, string):
        '''Recursive function to get all the key val pairs in each part'''
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


def setup(bot):
    bot.add_cog(Utility(bot))
