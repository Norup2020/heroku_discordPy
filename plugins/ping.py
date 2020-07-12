import discord
from discord.ext import commands

@commands.command()
async def ping(ctx):
    emb = discord.Embed(title='标题',description='描述',url='https://discordpy.readthedocs.io/en/latest/api.html#discord.Embed')
    emb.set_image(url='https://i1.hdslb.com/bfs/face/99bb8e6a7411b0bffb969b8c8440486a4a62f961.jpg_64x64.jpg')
    emb.set_thumbnail(url='https://i1.hdslb.com/bfs/face/99bb8e6a7411b0bffb969b8c8440486a4a62f961.jpg_64x64.jpg')
    emb.set_author(name='Toyomu', url=discord.Embed.Empty, icon_url=discord.Embed.Empty)
    await ctx.send(embed=emb)
    await ctx.send('{0.mention}pang you! \n {0.display_name}.'.format(ctx.author))
def setup(bot):
    bot.add_command(ping)