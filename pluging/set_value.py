# -*- coding: utf-8 -*-
from botpy.message import Message
from botpy.types.message import Embed, EmbedField

import redis
import re

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def admin_set(message:Message,members):
    #添加/扣除 UID、@xx 精神力、灵感能源 xxx
    msg = message.content
    s = re.split('\s+', msg)

    #判断正负
    if re.match(r"^.*(添加|增加).*$",msg):
        value = s[-1]
    if re.match(r"^.*(扣除|减少).*$",msg):
        value = str(-int(s[-1]))

    is_value = value.replace("-","")
    if is_value.isdigit() == False:
            return message.reply(content = "数值错误，请检查数值是否在最后且被空格隔开")
    ###################### id 列表 ###################### 
    id_list = []
    if members != 0:
        role = s[1]
        if role.isdigit() == False:
            return message.reply(content = "身份组id错误，请检查后重试")
        for user in members:
            if role in user["roles"]:
                id_list.append(user["user"]["id"])
    else:
        for i in s:
            if re.match(r"^\d{20}$", i):
                id_list.append(i)

        for i in message.mentions:
            id_list.append(i.id)
    ###################### id 列表 ###################### 
    attribute_list = ["精神力","灵感能源","点数","力量","体质","敏捷","外貌","智力","意志","城府","幸运"]
    for attribute in attribute_list:
        if attribute in msg:
            for id in id_list: 
                r.hincrby(f"Character_Attribute:{id}",attribute,value)
 
    if "积分" in msg:
        for id in id_list:
            r.zincrby("scoreboard:积分",value,f"{id}")

    return message.reply(content = "修改成功")
