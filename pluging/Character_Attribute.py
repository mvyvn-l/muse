# -*- coding: utf-8 -*-
from botpy.message import Message
from botpy.types.message import Embed, EmbedField

import redis
import re

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def my_Character_Attribute(message: Message):
        msg = message.content
        if r.hget(f"Character_Attribute:{message.author.id}","state") is None:
            r.hincrby(f"Character_Attribute:{message.author.id}","state",1)
            r.hincrby(f"Character_Attribute:{message.author.id}","count",350)
            r.hincrby(f"Character_Attribute:{message.author.id}","力量",0)
            r.hincrby(f"Character_Attribute:{message.author.id}","体质",0)
            r.hincrby(f"Character_Attribute:{message.author.id}","敏捷",0)
            r.hincrby(f"Character_Attribute:{message.author.id}","外貌",0)
            r.hincrby(f"Character_Attribute:{message.author.id}","智力",0)
            r.hincrby(f"Character_Attribute:{message.author.id}","意志",0)
            r.hincrby(f"Character_Attribute:{message.author.id}","城府",0)
            r.hincrby(f"Character_Attribute:{message.author.id}","幸运",50)
            r.hincrby(f"Character_Attribute:{message.author.id}","精神力",105500)
            r.hincrby(f"Character_Attribute:{message.author.id}","灵感能源",250500)
            r.hincrby(f"Character_Attribute:{message.author.id}","权限",0)

        '''     todo：权限判定
        if "4" in message.member.roles:
            role="？？？"
        elif "2" in message.member.roles:
            role="S"
        elif "11400150" in message.member.roles:
            role="A"
        elif "12597148" in message.member.roles:
            role="B"
        else:
            role="C"
        '''

        # 精神力等级判定
        jsl = r.hget(f"Character_Attribute:{message.author.id}","精神力")
        jsl = int(jsl)
        if jsl < 10000:
            jsldj = 0
            jsl1 = 10000
        elif 10000 <= jsl < 25000:
            jsldj = 1
            jsl1 = 25000
        elif 25000 <= jsl < 40000:
            jsldj = 2
            jsl1 = 40000
        elif 40000 <= jsl < 75000:
            jsldj = 3
            jsl1 = 75000
        elif 75000 <= jsl < 105000:
            jsldj = 4
            jsl1 = 105000
        elif 105000 <= jsl < 150000:
            jsldj = 5
            jsl1 = 150000
        elif 150000 <= jsl < 250000:
            jsldj = 6
            jsl1 = 250000
        elif 250000 <= jsl < 400000:
            jsldj = 7
            jsl1 = 400000
        elif 400000 <= jsl < 600000:
            jsldj = 8
            jsl1 = 600000
        elif 600000 <= jsl < 999999:
            jsldj = 9
            jsl1 = 999999
        elif 999999 < jsl:
            jsldj = 10
            jsl1 = 999999

        # 灵感能源等级判定
        lgny = r.hget(f"Character_Attribute:{message.author.id}","灵感能源")
        lgny = int(lgny)
        if lgny < 10000:
            lgnydj = 0
            lgny1 = 10000
        elif 10000 <= lgny < 25000:
            lgnydj = 1
            lgny1 = 25000
        elif 25000 <= lgny < 40000:
            lgnydj = 2
            lgny1 = 40000
        elif 40000 <= lgny < 75000:
            lgnydj = 3
            lgny1 = 75000
        elif 75000 <= lgny < 105000:
            lgnydj = 4
            lgny1 = 105000
        elif 105000 <= lgny < 150000:
            lgnydj = 5
            lgny1 = 150000
        elif 150000 <= lgny < 250000:
            lgnydj = 6
            lgny1 = 250000
        elif 250000 <= lgny < 400000:
            lgnydj = 7
            lgny1 = 400000
        elif 400000 <= lgny < 600000:
            lgnydj = 8
            lgny1 = 600000
        elif 600000 <= lgny < 999999:
            lgnydj = 9
            lgny1 = 999999
        elif 999999 < lgny:
            lgnydj = 10
            lgny1 = 999999

        ll=r.hget(f"Character_Attribute:{message.author.id}","力量")
        tz=r.hget(f"Character_Attribute:{message.author.id}","体质")
        mj=r.hget(f"Character_Attribute:{message.author.id}","敏捷")
        wm=r.hget(f"Character_Attribute:{message.author.id}","外貌")
        zl=r.hget(f"Character_Attribute:{message.author.id}","智力")
        yz=r.hget(f"Character_Attribute:{message.author.id}","意志")
        cf=r.hget(f"Character_Attribute:{message.author.id}","城府")
        xy=r.hget(f"Character_Attribute:{message.author.id}","幸运")
        jsl=r.hget(f"Character_Attribute:{message.author.id}","精神力")
        lgny=r.hget(f"Character_Attribute:{message.author.id}","灵感能源")

        embed = Embed(
        title=f"「人 物 面 板」",
        prompt="人物面板",
        thumbnail={"url": message.author.avatar},
        fields=[
            EmbedField(name=f"昵称：{message.author.username}"),
            EmbedField(name=f"力量：{ll}"),
            EmbedField(name=f"体质：{tz}"),
            EmbedField(name=f"敏捷：{mj}"),
            EmbedField(name=f"外貌：{wm}"),
            EmbedField(name=f"智力：{zl}"),
            EmbedField(name=f"意志：{yz}"),
            EmbedField(name=f"城府：{cf}"),
            EmbedField(name=f"幸运：{xy}"),
            EmbedField(name=f"精神力：{jsl}/{jsl1}({jsldj}/10)"),
            EmbedField(name=f"灵感能源：{lgny}/{lgny1}({lgnydj}/10)"),
        ],
        )
        return message.reply(embed=embed)
        
        return message.reply(content=f"""「{message.author.username}的人物面板」
生命：{r.hget(f"Character_Attribute:{message.author.id}","生命值")}/{r.hget(f"Character_Attribute:{message.author.id}","生命")}
智力：{r.hget(f"Character_Attribute:{message.author.id}","智力")}
武力：{r.hget(f"Character_Attribute:{message.author.id}","武力")}
敏捷：{r.hget(f"Character_Attribute:{message.author.id}","敏捷")}
防御：{r.hget(f"Character_Attribute:{message.author.id}","防御")}
精神力等级：{r.hget(f"Character_Attribute:{message.author.id}","精神力等级")}
权限等级：{role}""")

def add_count(message:Message):
    msg = message.content
    count_list = re.split('\s+', msg)
    
    #分割字符串
    if " " in count_list:
        count_list.remove(" ")

    #正则表达式判定
    pattern = "力量|体质|敏捷|外貌|智力|意志|城府"
    if re.search(pattern, count_list[1]):
        pass
    else:
        return message.reply(content="""所选择属性错误""")
    
    #负值改为正值
    if int(count_list[2]) < 0:
        count_list[2] = str(-int(count_list[2]))
    
    if int(count_list[2]) <= int(r.hget(f"Character_Attribute:{message.author.id}","count")):
        old = r.hget(f"Character_Attribute:{message.author.id}",f"{count_list[1]}")             #旧值
        r.hincrby(f"Character_Attribute:{message.author.id}",f"{count_list[1]}",count_list[2])  #写入
        new = r.hget(f"Character_Attribute:{message.author.id}",f"{count_list[1]}")             #新值
        count = -int(count_list[2])
        remain = r.hincrby(f"Character_Attribute:{message.author.id}","count", str(count))
        return message.reply(content=f"""加点成功
{count_list[1]}:{old}→{new}
剩余点数：{remain}""")
    else:
        return message.reply(content=f"点数不足")
    
def restart(message:Message):
    r.hset(f"Character_Attribute:{message.author.id}","state",1)
    r.hset(f"Character_Attribute:{message.author.id}","count",350)
    r.hset(f"Character_Attribute:{message.author.id}","力量",0)
    r.hset(f"Character_Attribute:{message.author.id}","体质",0)
    r.hset(f"Character_Attribute:{message.author.id}","敏捷",0)
    r.hset(f"Character_Attribute:{message.author.id}","外貌",0)
    r.hset(f"Character_Attribute:{message.author.id}","智力",0)
    r.hset(f"Character_Attribute:{message.author.id}","意志",0)
    r.hset(f"Character_Attribute:{message.author.id}","城府",0)
    r.hset(f"Character_Attribute:{message.author.id}","幸运",50)
    r.hset(f"Character_Attribute:{message.author.id}","精神力",105500)
    r.hset(f"Character_Attribute:{message.author.id}","灵感能源",250500)
    r.hset(f"Character_Attribute:{message.author.id}","权限",0)
    return message.reply(content = "重置成功")

def my_information(message:Message):
    score = int(r.zscore("scoreboard:积分", f"{message.author.id}"))
    count = r.hget(f"Character_Attribute:{message.author.id}","count")
    if "13428196" in message.member.roles:
        feast = "舒芙蕾"
    elif "13428198" in message.member.roles:
        feast = "高脚杯"
    else:
        feast = "无"
    
    # 遍历所有的 hash 表
    union ="无"
    for key in r.scan_iter('union:*'):
    # 查询该成员是否存在于当前的 hash 表中
        if r.hexists(key, f"member:{message.author.id}"):
            union = key.replace('union:', '')

    embed = Embed(
        title=f"{message.author.username}的信息详情",
        prompt="信息面板",
        thumbnail={"url": message.author.avatar},
        fields=[
            EmbedField(name=f"宴会选择：{feast}"),
            EmbedField(name=f"所属公会：{union}"),
            EmbedField(name=f"我的积分：{score}"),
            EmbedField(name=f"我的点数：{count}"),
        ],
    )
    return message.reply(embed=embed)