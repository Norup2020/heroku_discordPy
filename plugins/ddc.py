import discord
from discord.ext import commands


import requests
import datetime
import time
from functools import reduce

def ddc_fetcher(day:int = 1,*,fix:datetime.date=None,id:str=None):

    if day > 16:
        return '你想要我刷屏吗？'

    overflow = False

    today =  datetime.date.today() if not fix else fix # today

    next_month = datetime.date(today.year,today.month+1,1)

    offset = (next_month-today).days

    if day > offset:
        delta = day-offset
        overflow = True

    date = today.day


    url = 'https://api.live.bilibili.com/xlive/web-ucenter/v2/calendar/GetProgramList?type=1&year_month={}'.format(
        today.strftime("%Y-%m"))
    '''
    type=1 推荐查找
    type=2 我关注的主播（怎么可能会关注啦）
    type=3 精确查找（按uid）
    '''

    if id:
        url = 'https://api.live.bilibili.com/xlive/web-ucenter/v2/calendar/GetProgramList?type=3&year_month={}&ruids={}'.format(today.strftime("%Y-%m"),id)
    
    data = requests.get(url).json()

    name_list = data['data']['user_infos']

    info = lambda p : map(lambda x: {'name':name_list[str(x['ruid'])]['uname'],
        'title':x['title'],'id':x['room_id'],'time_h':time.localtime(x['start_time'])[3],
        'time_min':time.localtime(x['start_time'])[4],'Brecommand':x['is_recommend']},p)

    output = lambda p : reduce(lambda m,n:m+n , list(map(lambda x : '{5}[{0}]{5}{1}({2}:{3}){4}\n'.format(x['name'],
        x['title'],x['time_h'],x['time_min'] if x['time_min']!=0 else '00',
        '<id:{}>'.format(x['id']) if not id else '','**' if x['Brecommand'] == 1 else ''), info(p))))
    
    program_list = list(filter(lambda k: k != None, map(lambda x: f'{today.month}月' +  x + 
        '日:\n' + output(data['data']['program_infos'][x]['program_list']) if int(x) in range(date,date+day) else None,
        data['data']['program_infos'])))

    if fix:
        return (''.join(program_list),len(program_list))
    elif not overflow:
        length = len(program_list)
        if length != 0:
            return '近{}日结果:\n'.format(length) + ''.join(program_list)
        else:
            return '无结果，估计你的单推是懒狗'
    else:
        fixed = ddc_fetcher(delta,fix=next_month,id=id)
        length = len(program_list)+fixed[1]
        if length != 0:
            return '近{}日结果:\n'.format(len(program_list)+fixed[1]) + ''.join(program_list) + fixed[0]
        else:
            return '无结果，估计你的单推是懒狗'

@commands.command(aliases=('DD日历','dd_calendar'))
async def ddc(ctx,*args):
    '''
    原则上是 ddc [数字] [用户名]
    实际上你可以缺少一个
    移植过来的神奇产物
    '''
    digit = None
    sstr = None

    for i in args:
        if digit != None and sstr != None:
            break
        if i.isdigit():
            digit = i
        else:
            sstr = i

    if digit == None and sstr == None:
        msg = ddc_fetcher(1)
        await ctx.send(msg)
        return
    
    if sstr:
        name = str(sstr).replace('阿夸','阿库娅').replace('啊夸','阿库娅').replace('圣皇','阿库娅').replace('Aqua','阿库娅')
    

        header = {'Referer': 'https://search.bilibili.com/'}
        uid = requests.get(f'https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&page=1&order=fans&keyword={name}&order_sort=0&changing=mid',
            headers = header).json()['data']['result'][0]['mid']


        info_data = requests.get(f'https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp').json()['data']
        title = '查看 {} 的频道'.format(info_data['name'])
        uurl = f'https://space.bilibili.com/{uid}'
        desc = info_data['sign']
        photo = info_data['face'].replace('http://','https://')
        top = info_data['top_photo'].replace('http://','https://')
    
        emb = discord.Embed(title=title,description=desc,url=uurl)
        emb.set_thumbnail(url=photo)
        emb.set_image(url=top)
        await ctx.send(embed=emb)
        
        if digit:
            msg = ddc_fetcher(int(digit),id=uid)
        else:
            msg = ddc_fetcher(id=uid)
    else:
        msg = ddc_fetcher(int(digit))
    
    await ctx.send(msg)
    return


def setup(bot):
    bot.add_command(ddc)