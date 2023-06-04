# -*- coding: utf-8 -*-
from botpy.message import Message
from botpy.types.message import Embed, EmbedField

import redis
import requests
import re

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def rua(message: Message):
    profile = message.mentions[0].avatar

    url = "http://api.wer.plus/api/ruad?url="
    url = url + profile
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()["url"]
        return message.reply(image = data)
    else:
        print("Error:", response.status_code)

def role_list(message:Message,role_list):
    s=""
    role_list = role_list["roles"]
    for role in role_list:
        name = role["name"]
        role_id = role["id"]
        s += f"「{name}」id:{role_id}\n"
    s = s.rstrip("\n")
    return message.reply(content = s)

