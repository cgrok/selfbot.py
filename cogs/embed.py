import discord
from discord.ext import commands
import datetime
import time


class Embed():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,description='Do .embed to see how to use it.')
    async def embed(self, ctx, *, msg: str = None):
        '''Embed complex rich embeds as the bot.'''
        try:
            
            if msg:
                ptext = title = description = image = thumbnail = color = footer = author = None
                timestamp = discord.Embed.Empty
                def_color = False
                embed_values = msg.split('|')
                for i in embed_values:
                    if i.strip().lower().startswith('ptext='):
                        if i.strip()[6:].strip() == 'everyone':
                            ptext = '@everyone'
                        elif i.strip()[6:].strip() == 'here':
                            ptext = '@here'
                        else:
                            ptext = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('title='):
                        title = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('description='):
                        description = i.strip()[12:].strip()
                    elif i.strip().lower().startswith('desc='):
                        description = i.strip()[5:].strip()
                    elif i.strip().lower().startswith('image='):
                        image = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('thumbnail='):
                        thumbnail = i.strip()[10:].strip()
                    elif i.strip().lower().startswith('colour='):
                        color = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('color='):
                        color = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('footer='):
                        footer = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('author='):
                        author = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('timestamp'):
                        timestamp = ctx.message.timestamp

                    if color:
                        if color.startswith('#'):
                            color = color[1:]
                        if not color.startswith('0x'):
                            color = '0x' + color

                    if ptext is title is description is image is thumbnail is color is footer is author is None and 'field=' not in msg:
                        await self.bot.delete_message(ctx.message)
                        return await self.bot.send_message(ctx.message.channel, content=None,
                                                           embed=discord.Embed(description=msg))

                    if color:
                        em = discord.Embed(timestamp=timestamp, title=title, description=description, color=int(color, 16))
                    else:
                        em = discord.Embed(timestamp=timestamp, title=title, description=description)
                    for i in embed_values:
                        if i.strip().lower().startswith('field='):
                            field_inline = True
                            field = i.strip().lstrip('field=')
                            field_name, field_value = field.split('value=')
                            if 'inline=' in field_value:
                                field_value, field_inline = field_value.split('inline=')
                                if 'false' in field_inline.lower() or 'no' in field_inline.lower():
                                    field_inline = False
                            field_name = field_name.strip().lstrip('name=')
                            em.add_field(name=field_name, value=field_value.strip(), inline=field_inline)
                    if author:
                        if 'icon=' in author:
                            text, icon = author.split('icon=')
                            if 'url=' in icon:
                                print("here")
                                em.set_author(name=text.strip()[5:], icon_url=icon.split('url=')[0].strip(), url=icon.split('url=')[1].strip())
                            else:
                                em.set_author(name=text.strip()[5:], icon_url=icon)
                        else:
                            if 'url=' in author:
                                print("here")
                                em.set_author(name=author.split('url=')[0].strip()[5:], url=author.split('url=')[1].strip())
                            else:
                                em.set_author(name=author)

                    if image:
                        em.set_image(url=image)
                    if thumbnail:
                        em.set_thumbnail(url=thumbnail)
                    if footer:
                        if 'icon=' in footer:
                            text, icon = footer.split('icon=')
                            em.set_footer(text=text.strip()[5:], icon_url=icon)
                        else:
                            em.set_footer(text=footer)
                await self.bot.send_message(ctx.message.channel, content=ptext, embed=em)
            else:
                msg = '*Params:*\n```bf\n[title][author][desc][field][footer][thumbnail][image][timestamp][ptext]```'
                await self.bot.send_message(ctx.message.channel, msg)
            try:
                await self.bot.delete_message(ctx.message)
            except:
                pass
        except:
            await self.bot.send_message(ctx.message.channel, 'looks like something fucked up. or i dont have embed perms')
               
            

def setup(bot):
    bot.add_cog(Embed(bot))
