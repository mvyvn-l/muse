# -*- coding: utf-8 -*-
from botpy.message import Message
from botpy.types.message import Embed, EmbedField

import redis
import re

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def b_q(uchar):
    """单个字符 半角转全角"""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e: # 不是半角字符就返回原来的字符
        return uchar 
    if inside_code == 0x0020: # 除了空格其他的全角半角的公式为: 半角 = 全角 - 0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return chr(inside_code)

def give(message:Message):
    msg = message.content
    if msg[0:2] == '给予' :
        goods = re.split('\s+', msg)
        r.hincrby(f"backpack:{message.mentions[0].id}",f"{goods[1]}",amount=goods[2])
        return message.reply(content=f'''已给予{message.mentions[0].username}
物品：{goods[1]}
数量：{goods[2]}''')
        
def del_goods(message:Message):
    msg = message.content
    if msg[0:2] == '丢弃' :
        goods = re.split('\s+', msg)
        if int(goods[2]) < 0:
            goods[2] = -int(goods[2])
        if r.hget(f"backpack:{message.author.id}",f"{goods[1]}") == None:
            return message.reply(content = f"您的背包中还没有 {goods[1]}")
        if int(r.hget(f"backpack:{message.author.id}",f"{goods[1]}")) < int(goods[2]):
            return message.reply(content = f"您的背包中没有足够的 {goods[1]} 可以丢弃")
        if int(r.hget(f"backpack:{message.author.id}",f"{goods[1]}")) == int(goods[2]):
            r.hdel(f"backpack:{message.author.id}",f"{goods[1]}")   #清除键-值
        else:
            r.hincrby(f"backpack:{message.author.id}",f"{goods[1]}",amount=(-int(goods[2])))
        return message.reply(content=f'''{message.author.username}丢弃了 {goods[1]}
数量：{goods[2]}''')
    
def buy_goods(message:Message):

    msgs = message.content
    msg = re.split('\s+', msgs)

    if r.hget(f"store_list",f"{msg[1]}") == "0" or r.hget(f"store_list",f"{msg[1]}") == None:
        return message.reply(content = "商品不存在")
    if int(r.hlen(f"backpack:{message.author.id}")) >= 20:
        if r.hget(f"backpack:{message.author.id}",f"{msg[1]}"):
            pass
        else:
            return message.reply(content = "背包已满")
    score = r.zscore("scoreboard:积分", f"{message.author.id}")
    value = int(r.hget(f"store:{msg[1]}","价格"))
    number = int(r.hget(f"store:{msg[1]}","数量"))
    limit = int(r.hget(f"store:{msg[1]}","限购"))
    if msgs[0:2] == '购买' :
        if value == -1:
            return message.reply(content = "您没有足够的积分购买此商品")
        if value * int(msg[2]) > int(score):
            return message.reply(content = "您没有足够的积分购买此商品")
        if number == -1:
            number = int(msg[2])
        if number == 0:
            return message.reply(content = "此商品供货不足")
        if number < int(msg[2]):
            return message.reply(content = "此商品供货不足")
        if limit == -1:
            limit = int(msg[2])
        elif limit < int(msg[2]) + int(r.hget(f"backpack:{message.author.id}",f"{msg[1]}")):
            x = int(r.hget(f"store:{msg[1]}","限购")) 
            return message.reply(content = f"此商品每人限购{x}件")
        elif limit < int(msg[2]):
            x = int(r.hget(f"store:{msg[1]}","限购")) 
            return message.reply(content = f"此商品每人限购{x}件")
        if int(r.hget(f"store:{msg[1]}","数量")) != -1:
            r.hincrby(f"store:{msg[1]}","数量",amount=(-int(msg[2]))) 
        r.hincrby(f"backpack:{message.author.id}",f"{msg[1]}",amount=int(msg[2]))

        r.zincrby("scoreboard:积分",-value * int(msg[2]),f"{message.author.id}")
        return message.reply(content = f"{message.author.username}购买了{msg[2]}件{msg[1]}")
    
def my_backpack(message:Message):
    #backpack = r.hgetall(f"backpack:{message.author.id}")   #获取所有物品
    #blen=r.hlen(f"backpack:{message.author.id}")            #物品种类数量
    key=r.hkeys(f"backpack:{message.author.id}")            #键--物品名称
    val=r.hvals(f"backpack:{message.author.id}")            #值--物品数量
    
    keys=["〔空〕"] * 20
    vals=[""] * 20
    count = 0
    for s in key:
        vals[count] = val[count]
        keys[count] = ""
        for i in s:
            keys[count] += b_q(i)
        count += 1

    embed = Embed(
    title=f"{message.author.username}的背包",
    thumbnail={"url": "https://pic.imgdb.cn/item/64315f790d2dde5777c1388b.png"},
    prompt=f"{message.author.username}的背包",
    fields=[
        EmbedField(name="{:　<13s}{}".format("物品","数量")),
        EmbedField(name="{:　<13s}{}".format(keys[0],vals[0])),
        EmbedField(name="{:　<13s}{}".format(keys[1],vals[1])),
        EmbedField(name="{:　<13s}{}".format(keys[2],vals[2])),
        EmbedField(name="{:　<13s}{}".format(keys[3],vals[3])),
        EmbedField(name="{:　<13s}{}".format(keys[4],vals[4])),
        EmbedField(name="{:　<13s}{}".format(keys[5],vals[5])),
        EmbedField(name="{:　<13s}{}".format(keys[6],vals[6])),
        EmbedField(name="{:　<13s}{}".format(keys[7],vals[7])),
        EmbedField(name="{:　<13s}{}".format(keys[8],vals[8])),
        EmbedField(name="{:　<13s}{}".format(keys[9],vals[9])),
        EmbedField(name="{:　<13s}{}".format(keys[10],vals[10])),
        EmbedField(name="{:　<13s}{}".format(keys[11],vals[11])),
        EmbedField(name="{:　<13s}{}".format(keys[12],vals[12])),
        EmbedField(name="{:　<13s}{}".format(keys[13],vals[13])),
        EmbedField(name="{:　<13s}{}".format(keys[14],vals[14])),
        EmbedField(name="{:　<13s}{}".format(keys[15],vals[15])),
        EmbedField(name="{:　<13s}{}".format(keys[16],vals[16])),
        EmbedField(name="{:　<13s}{}".format(keys[17],vals[17])),
        EmbedField(name="{:　<13s}{}".format(keys[18],vals[18])),
        EmbedField(name="{:　<13s}{}".format(keys[19],vals[19])),
    ],
    )
    return message.reply(embed=embed)