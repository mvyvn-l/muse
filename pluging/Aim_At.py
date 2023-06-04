# -*- coding: utf-8 -*-

from botpy.message import Message

import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def aim_at(message:Message):
    msg = message.content
    if "取消" in msg:
        a=0
    else:
        a=1
    x=message.mentions[0].id
    if message.mentions[0].id == "15972689532541219830":
        return message.reply(content=f"大不敬")
    r.hset("aim_at",f"{x}",f"{a}")
    if a==1:
        return message.reply(content=f"闭嘴吧你<@!{x}>")
    else:
        return message.reply(content=f"放你一马<@!{x}>")
    
def detection(message:Message):
    x = message.author.id
    return r.hget("aim_at",f"{x}")
    