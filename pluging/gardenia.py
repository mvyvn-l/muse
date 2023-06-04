
from botpy.message import Message
from botpy.message import DirectMessage
from botpy.types.message import Embed, EmbedField

import redis
import random

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def water(message: Message):
        favtime=r.ttl(f"gardenia:{message.author.id}time")
        if favtime == -2:
            fav=random.randint(1,3)
            r.hincrby(f"gardenia:{message.author.id}","favorability",f"{fav}")
            r.setex(f"gardenia:{message.author.id}time",21600,"time")
            r.zincrby("scoreboard:积分",f"{fav}",f"{message.author.id}")
            favall = r.hget(f"gardenia:{message.author.id}","favorability")
            if int(favall) < 30:
                state="发芽期"
                remain=30
            elif 30 <= int(favall) < 60:
                state="展叶期"
                remain=60
            elif 60 <= int(favall) <100:
                state="开花期"
                remain=100
            elif 100 <= int(favall) <150:
                state="小花妖"
                remain=150
            elif 150 <= int(favall)<300:
                state="花妖族长"
                remain=300
            elif 300 <= int(favall):
                state="花仙"
                remain=800

            embed = Embed(
            title=f"{message.author.username}的栀子花浇水成功",
            prompt="栀子花浇水成功",
            thumbnail={"url": "https://gd-hbimg.huaban.com/ad501812efe59dd49231b47d322cee4b128541202df7a-EIEBQx"},
            fields=[
                EmbedField(name=f"积分+{fav}"),
                EmbedField(name=f"好感度+{fav}"),
                EmbedField(name=f"当前好感度为:{favall}/{remain}"),
                EmbedField(name=f"当前状态：{state}"),
            ],
            )
            return message.reply(embed=embed)

            return message.reply(content=f'''栀子花浇水成功
好感度+{fav}
当前好感度为:{favall}/{remain}
当前状态：{state}''')
        else:
            favtime=r.ttl(f"gardenia:{message.author.id}time")
            shi=favtime//3600
            fen=favtime%3600//60
            miao=favtime%60
            return message.reply(content=f"距离下次浇水还有：{shi}时{fen}分{miao}秒")


def my_gardenia(message: Message):
        favall = r.hget(f"gardenia:{message.author.id}","favorability")
        if int(favall) < 30:
            state="发芽期"
            remain=30
        elif 30 <= int(favall) < 60:
            state="展叶期"
            remain=60
        elif 60 <= int(favall) <100:
            state="开花期"
            remain=100
        elif 100 <= int(favall) <150:
            state="小花妖"
            remain=150
        elif 150 <= int(favall)<300:
            state="花妖族长"
            remain=300
        elif 300 <= int(favall):
            state="花仙"
            remain=800

        embed = Embed(
            title=f"{message.author.username}的栀子花",
            prompt="栀子花浇水成功",
            thumbnail={"url": "https://gd-hbimg.huaban.com/ad501812efe59dd49231b47d322cee4b128541202df7a-EIEBQx"},
            fields=[
                EmbedField(name=f"当前好感度为:{favall}/{remain}"),
                EmbedField(name=f"当前状态：{state}"),
            ],
            )
        return message.reply(embed=embed)
        return message.reply(content=f'''{message.author.username}的栀子花
当前好感度为:{favall}/{remain}
当前状态：{state}''')
