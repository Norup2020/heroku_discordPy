import discord
from discord.ext import commands

import re
from random import randint

class Invalid_Express(Exception):
    pass

class Out_of_range(Exception):
    pass

class Zero_error(Exception):
    pass

class Overflow(Exception):
    pass

class Illegal_Express(Exception):
    pass

DEFAULT_ERROR_LIST = ['你就不能输入正常一点的表达式吗？',
'如果你有这么多面数的骰子，那我希望它没有；如果你没有，那我希望有',
'那你给我弄个零面骰子！','我没那么多骰子']

DEFAULT_REPLY_LIST = ['掷骰','掷骰']


async def roll_dice(usr,inp:str,error_list = DEFAULT_ERROR_LIST,reply_list = DEFAULT_REPLY_LIST):
    eps = ''
    act = ''
    try:
        eps,act = inp.split(' ',1)
    except:
        eps = inp
    # 怎么还是else
    #crt_exp = crt_analyze(eps)
    try:
        crt_exp = crt_analyze(eps)
    except Illegal_Express:
        deres = randint(1,100)
        return f'**{usr}**{reply_list[0]} {inp}: D100 = **{deres}**'
    except Invalid_Express:
        return error_list[0]
    except Out_of_range:
        return error_list[1]
    except Zero_error:
        return error_list[2]
    except Overflow:
        return error_list[3]
    return '**{}**{}: {}'.format(usr,reply_list[0],crt_exp) if not act \
                else '**{}**{} {}: {}'.format(usr,reply_list[1],act,crt_exp)

def crt_analyze(inp):
    patten = re.compile(r'[0-9]*[dD][0-9]+|[\+\*\-\/]+|[0-9]*')
    process_list = re.findall(patten,inp)
    dice_list = ''
    show_list = ''
    res = ''

    frt_dice = 0
    frt_opr = 0

    if not process_list[0]:
        raise Illegal_Express

    for i in process_list:

        if re.match(r'[0-9]*[dD][0-9]+', i):
            frt_opr += 1
            if frt_dice >= 1:
                raise Invalid_Express
            frt_dice += 1
            show_list += dice(i)  ##数字，列出的算式，如果是D100输入输出就是出来的随机数
            dice_list += i.upper() ##骰子的名称，如‘D100’
            continue

        elif re.match(r'[\+\*\-\/]+',i):
            frt_opr = 0
            frt_dice = 0
            if frt_opr >= 1:
                raise Invalid_Express
            show_list += i[0]
            dice_list += i[0]
            continue

        elif re.match(r'[0-9]*',i):
            show_list += i
            dice_list += i
            continue
    
    if not show_list or not re.match(r'[0-9]*[dD][0-9]+', dice_list):
        raise Illegal_Express


    if re.match(r'.*[\+\*\-\/]+.*', show_list):
        #res = int(eval(show_list))1
        try:
            res = int(eval(show_list))
        except:
            raise Invalid_Express
        else:
            return '{} = {} = **{}**'.format(dice_list,show_list,res)
    
    return '{} = **{}**'.format(dice_list,show_list)



def dice(inp:str,*,default = 100,maxi_planes = 10000,maxi_pieces = 50):

    dice = inp.upper()
    pieces = dice[0:dice.find('D')]

    planes = default

    if len(inp) > 0:
        planes = int(dice[dice.find('D') + 1 :])

    if planes > maxi_planes:
        raise Out_of_range
    if planes == 0:
        raise Zero_error
    
    res = str( randint( 1,planes ) )
    
    if not pieces:
        return res
    else:
        pieces = int(pieces)

    if pieces > maxi_pieces:
        raise Overflow
    
    res = ''
    for i in range(pieces):
        once = str( randint( 1,planes ) )
        res += f'{once}+'

    return (res[:-1])



@commands.command(name='rh',aliases=('roll_hide',))
async def roll_dice_command_hide(ctx,*,arg):
    '''扔出私骰,和r命令差不多'''
    user = ctx.author.display_name
    message = await roll_dice(user,arg,reply_list=['掷出暗骰','掷出暗骰，出于'])
    await ctx.author.send(message)

@commands.command(name='ra',aliases=('roll_skil','rc'))
async def roll_dice_command_skill(ctx,*args):
    '''技能判定 rc/ra [技能名称] [技能成功率]'''
    user = ctx.author.display_name
    skill = 60
    if len(args) == 1 and args[0].isdigit():
        skill = int(args[0])
    if len(args) == 1 and not args[0].isdigit():
        await ctx.send('你都没设定好**{}**的成功率, 我怎么判定'.format(args[0]))
        return

    res = randint( 1,100 )
    if res > skill:
        status = '失败'
        if res >= 96:
            status = '大失败'
    else:
        if res <= 5:
            status = '大成功'
        elif res < skill//5:
            status = '极难成功'
        elif res < skill//2:
            status = '困难成功'
        else:
            status = '成功'

    message = f'{user}进行检定 D100 = **{res}/{skill}** ***{status}***'
    await ctx.send(message)


#无论如何你都要吧别名弄成(str,)的形式，否则会解体

@commands.command(name='r',aliases=('roll','rd'))
async def roll_dice_command(ctx,*,arg):
    '''扔出骰子 r [骰子表达式]
    [骰子表达式] : xDy(+\-\*\\ mdn)'''
    user = ctx.author.display_name
    message = await roll_dice(user,arg)
    await ctx.send(message)

@commands.command(name='sc',aliases=('san_check',))
async def san_check(ctx,*,arg):
    '''sc [骰子表达式1]/[骰子表达式2] [san值]
    [骰子表达式] : xDy(+\-\*\\ mdn)'''
    user = ctx.author.display_name
    exp,san = arg.split()
    if san == '' or not san.isdigit():
        await ctx.send('未设定San值, San值需要为1~100的整数')
        return
    san = int(san)
    if san < 1 or san > 100:
        await ctx.send('San值需要为1~100的整数, 有这样的San值, 怎么能跑好团呢')
        return
    
    dices = exp.split('/')
    if len(dices) < 2:
        await ctx.send('你连斜杠都不会打吗')
        return
    
    sc_res = randint( 1,100 )
    dice = None
    san_res = ''
    if sc_res > san:
        dice = dices[1].upper()
        san_res = '失败'
    else:
        dice = dices[0].upper()
        san_res = '成功'
    
    judge = crt_analyze(dice)
    amount = re.match(r'.*\*\*(.*)\*\*.*', judge).group(1)
    final_san = san - int(amount)
    
    message = f'**{user}** 的san check: \n1D100 = {sc_res}/{san} {san_res}\n{user}的san值减少**{judge}**点, 当前剩余**{final_san}**点'
    await ctx.send(message)
    san = final_san

def setup(bot):
    bot.add_command(roll_dice_command)
    bot.add_command(roll_dice_command_skill)
    bot.add_command(roll_dice_command_hide)
    bot.add_command(san_check)