import discord
from discord.ext import commands
from io import BytesIO
import requests

@commands.command(name='随机图片')
async def rand_pic(ctx):
    image_type = ".tmp"
    try:
        web = requests.get('http://193.112.67.15/setuapi/discovery').json()
        url = web['0']['url_big'].replace("pximg.net", "pixiv.cat")
        
        await ctx.send(f"PID:{str(web['0']['id'])}\n若图片发不出来请自行查看")
        
        web_image = requests.get(url, timeout=10)
        
        if web_image.status_code == 200:
            if url.find(".jpg") != -1:
                image_type = ".jpg"
            elif url.find(".png") != -1:
                image_type = ".png"
            try:
                await ctx.send(file=discord.File(BytesIO(web_image.content),filename=f'pic{image_type}'))
            except Exception as E:
                await ctx.send(f'An exception occured:\n{E}')
        else:
            await ctx.send('网络错误，服务器返回:%s' % web_image.status_code)
    except:
        pass
    return 

def setup(bot):
    bot.add_command(rand_pic)