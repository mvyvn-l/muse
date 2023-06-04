# -*- coding: utf-8 -*-
import asyncio
from botpy.message import Message
from botpy.types.message import Embed, EmbedField

import redis
import re
import json
import numpy as np
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import matplotlib.backends.backend_agg as agg
import os
import glob

from selenium import webdriver
from selenium.webdriver.edge.options import Options


pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def judge_condition(condition_list,message:Message):
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

        is_condition = True

        for condition in condition_list:
            if "0" == condition:
                return True
            if "力量" in condition:
                key = ll
                key_name = "力量"
            if "体质" in condition:
                key = tz
                key_name = "体质"
            if "敏捷" in condition:
                key = mj
                key_name = "敏捷"
            if "外貌" in condition:
                key = wm
                key_name = "外貌"
            if "智力" in condition:
                key = zl
                key_name = "智力"
            if "意志" in condition:
                key = yz
                key_name = "意志"
            if "城府" in condition:
                key = cf
                key_name = "城府"
            if "幸运" in condition:
                key = xy
                key_name = "幸运"
            if "精神力" in condition:
                key = jsl
                key_name = "精神力"
            if "灵感能源" in condition:
                key = lgny
                key_name = "灵感能源"
            if key == None:
                return "1"
            value = re.findall('\d+\.\d+', condition)
            value = str(condition)
            value = value.replace(key_name,"")
            value = value.replace(" ","")
            value = value.replace(">","")
            value = value.replace("<","")
            value = value.replace("=","")
            value = int(value)
            key = int(key)

            if ">" in condition:
                if key > value:
                    pass
                else:
                    is_condition = False
            if ">=" in condition:
                if key >= value:
                    pass
                else:
                    is_condition = False
            if "<" in condition:
                if key < value:
                    pass
                else:
                    is_condition = False
            if "<=" in condition:
                if key <= value:
                    pass
                else:
                    is_condition = False
            if "=" in condition:
                if key == value:
                    pass
                else:
                    is_condition = False
            if "!=" in condition:
                if key != value:
                    pass
                else:
                    is_condition = False

        return is_condition #返回值
             
def set_value(value_dirt,message:Message):
    s=""
    for key in value_dirt:
        value = int(value_dirt[key])
        if "0" == key:
            return ""
        if "力量" in key:
            r.hincrby(f"Character_Attribute:{message.author.id}","力量",value)
        if "体质" in key:
            r.hincrby(f"Character_Attribute:{message.author.id}","体质",value)
        if "敏捷" in key:
            r.hincrby(f"Character_Attribute:{message.author.id}","敏捷",value)
        if "外貌" in key:
            r.hincrby(f"Character_Attribute:{message.author.id}","外貌",value)
        if "智力" in key:
            r.hincrby(f"Character_Attribute:{message.author.id}","智力",value)
        if "意志" in key:
            r.hincrby(f"Character_Attribute:{message.author.id}","意志",value)
        if "城府" in key:
            r.hincrby(f"Character_Attribute:{message.author.id}","城府",value)
        if "幸运" in key:
            r.hincrby(f"Character_Attribute:{message.author.id}","幸运",value)
        if "精神力" in key:
            r.hincrby(f"Character_Attribute:{message.author.id}","精神力",value)
        if "灵感能源" in key:
            r.hincrby(f"Character_Attribute:{message.author.id}","灵感能源",value)
        if "点数" in key:
            r.hincrby(f"Character_Attribute:{message.author.id}","count",value)
        if value > 0:
            s += f"\n{key}+{value}"
        if value < 0:
            s += f"\n{key}{value}"
    return s

# def ectype_create(message: Message,msg):  #创建副本（废弃）
#         msg = msg["message"]["content"]
#         #msg = msg.encode('unicode_escape').decode()
#         try:
#             json.loads(msg)
#             print("字符串符合JSON格式")
#         except json.decoder.JSONDecodeError as e:
#             return message.reply(content = f"JSON格式不正确\n异常信息:\n{e}")

#         json_data = json.loads(msg)
#         title = json_data["title"]
#         print(title)
#         r.hset(f"ectype:ectype",f"{title}","1")
#         r.set(f"ectype:{title}",msg)
#         return message.reply(content = f"成功创建副本『{title}』")

def ectype_reload(message:Message):     #更新副本

    # 填写要打开所有文件的目录路径及文件类型
    dir_path = 'muse\pluging\json'
    file_extension = '*.json'

    # 遍历目录及子目录下的所有文件
    for filename in glob.iglob(os.path.join(dir_path, '**', file_extension), recursive=True):
        with open(filename,encoding="utf-8") as ectype:
            data = ectype.read()
            try:
                json_data = json.loads(data)
                print("字符串符合JSON格式")
            except json.decoder.JSONDecodeError as e:
                return message.reply(content = f"{filename}的JSON格式不正确\n异常信息:\n{e}")
        title = json_data["title"]
        if r.hget(f"ectype:ectype",f"{title}") == None:
            r.hset(f"ectype:ectype",f"{title}","1")
        #r.set(f"ectype:{title}",ectype)
    ectype_list_name = r.hgetall("ectype:ectype")
    for ectype_name in ectype_list_name:
        files = glob.glob(os.path.join(dir_path, f"{ectype_name}.json"))
        if len(files) > 0:
            pass
        else:
            r.hdel("ectype:ectype",ectype_name)
    return message.reply(content = f"成功更新副本")

def ectype_list(message:Message):   #副本目录
    list_ectype = r.hgetall("ectype:ectype")
    s = "『副本目录』"
    print(list_ectype)
    for title in list_ectype:
        if r.hget("ectype:ectype",f"{title}") == "1":
            state = "开启"
        if r.hget("ectype:ectype",f"{title}") == "0":
            state = "关闭"
        s += f"\n{title} （{state}）"
    #s = s.rstrip('\n')
    return message.reply(content = s)


def ectype_into(message:Message,dms):
    msg = message.content

    #判断是否处在副本内
    if r.hget(f"ectype:user:{message.author.id}","state") == "1":
        return message.reply(content = "你目前正在副本内，无法开启新副本")
    
    #去除消息前缀
    if "进入副本 " in msg:
        msg = msg.replace("进入副本 ","")
    else:
        msg = msg.replace("进入副本","")

    #判断副本是否存在
    if r.hget(f"ectype:ectype",msg) == None:
        return message.reply(content = f"副本『{msg}』不存在")
    try:
        dms == 1
    except:
        dms == None
    #判定副本是否开启
    if dms != None:
        if r.hget("ectype:ectype",f"{msg}") == "0":
            return message.reply(content = f"副本『{msg}』已关闭")
    else:
        roles = message.member.roles
        if "4" in roles or "2" in roles:
            pass
        else:
            if r.hget("ectype:ectype",f"{title}") == "0":
                return message.reply(content = f"副本『{msg}』已关闭")

    #读取副本JSON数据
    with open(f'muse\pluging\json\{msg}.json', encoding='UTF-8',errors='ignore') as ectype:
        ectype = ectype.read()
        ectype_data = json.loads(ectype)

    
    title = ectype_data["title"]                        #标题
    content = ectype_data["line"]["1"]["content"]       #内容
    option_list = ectype_data["line"]["1"]["option"]    #选项

    #选项内容
    option =""
    for key in option_list:
        option_content = ectype_data["line"]["1"]["option"][key]["content"]
        option += f"{key}:{option_content}\n"
    option = option.rstrip('\n')


    r.hset(f"ectype:user:{message.author.id}","state","1")          #写入状态
    r.hset(f"ectype:user:{message.author.id}","ectype",f"{title}")  #写入正在进行的副本标题
    r.hset(f"ectype:user:{message.author.id}","line",f"1")          #写入剧情线

    #回复消息
    return message.reply(content = f"""『{title}』
{content}
{option}""")

def ectype_judge(message:Message,dms):
    msg = message.content
    id = message.author.id

    title = r.hget(f"ectype:user:{message.author.id}","ectype")     #获取标题
    line = r.hget(f"ectype:user:{message.author.id}","line")        #获取剧情线
    #读取副本JSON数据
    with open(f'muse\pluging\json\{title}.json', encoding='UTF-8',errors='ignore') as ectype:
        ectype = ectype.read()
        ectype_data = json.loads(ectype)

    try:
        dms == 1
    except:
        dms == None
    #判定副本是否开启
    if dms != None:
        if r.hget("ectype:ectype",f"{title}") == "0":
            return message.reply(content = f"副本『{title}』已关闭")
    else:
        roles = message.member.roles
        if "4" in roles or "2" in roles:
            pass
        else:
            if r.hget("ectype:ectype",f"{title}") == "0":
                return message.reply(content = f"副本『{title}』已关闭")
    is_end = 0

    try:
        ectype_data["line"][line]["option"][msg] is not None
        is_continue = True
    except:
        is_continue = False

    if is_continue == True:
        ectype_state = r.hget(f"ectype:user:{message.author.id}",f"{title}")
        condition_list = ectype_data["line"][line]["option"][msg]["condition"]["content"]   #选项条件列表
        is_condition = judge_condition(condition_list,message)  #选项条件判定
        if is_condition == "1":
            return message.reply(content = "请先查看属性面板，在图灵区输入[我的属性]即可")
        value_content = ""
        if is_condition == True:
            next_line = ectype_data["line"][line]["option"][msg]["condition"]["True"]["skip"]
            value_dirt = ectype_data["line"][line]["option"][msg]["condition"]["True"]["value"]
            if ectype_state != "1":
                value_content = set_value(value_dirt,message)
        if is_condition == False:
            next_line = ectype_data["line"][line]["option"][msg]["condition"]["False"]["skip"]
            value_dirt = ectype_data["line"][line]["option"][msg]["condition"]["False"]["value"]
            if ectype_state != "1":
                value_content = set_value(value_dirt,message)
        r.hset(f"ectype:user:{message.author.id}","line",f"{next_line}")

        if ectype_data["line"][next_line].get("end") is not None:                #判断是否为结局
            r.hset(f"ectype:user:{message.author.id}","state","0")
            is_end = 1
            value_content_end = "无"
            if ectype_state != "1":
                value_dirt = ectype_data["line"][next_line]["value"]
                value_content_end = set_value(value_dirt,message)
                r.hset(f"ectype:user:{message.author.id}",f"{title}","1")
    else:
        return asyncio.sleep(0)

    line = r.hget(f"ectype:user:{message.author.id}","line")
    title = ectype_data["title"]
    content = ectype_data["line"][line]["content"]
    
    if is_end:
        end = ectype_data["line"][line]["end"]
        return message.reply(content = f"""『{title}』{value_content}
{content}
{end}
奖励结算：{value_content_end}""")
    else:#非结局回复
        option_list = ectype_data["line"][line]["option"]
        option =""
        for key in option_list:
            option_content = ectype_data["line"][line]["option"][key]["content"]
            option += f"{key}:{option_content}\n"
        option = option.rstrip('\n')
        return message.reply(content = f"""『{title}』{value_content}
{content}
{option}""")

def now_ectype(message:Message,dms):

    #判断是否处在副本内
    if r.hget(f"ectype:user:{message.author.id}","state") == "0":
        return message.reply(content = "你还没有进入副本呢")
    
    title = r.hget(f"ectype:user:{message.author.id}","ectype")     #获取标题
    line = r.hget(f"ectype:user:{message.author.id}","line")        #获取剧情线

    try:
        dms == 1
    except:
        dms == None
    #判定副本是否开启
    if dms != None:
        if r.hget("ectype:ectype",f"{title}") == "0":
            return message.reply(content = f"副本『{title}』已关闭")
    else:
        roles = message.member.roles
        if "4" in roles or "2" in roles:
            pass
        else:
            if r.hget("ectype:ectype",f"{title}") == "0":
                return message.reply(content = f"副本『{title}』已关闭")
    #读取副本JSON数据
    with open(f'muse\pluging\json\{title}.json', encoding='UTF-8',errors='ignore') as ectype:
        ectype = ectype.read()
        ectype_data = json.loads(ectype)
    title = ectype_data["title"]
    content = ectype_data["line"][line]["content"]
    option_list = ectype_data["line"][line]["option"]
    option =""
    for key in option_list:
        option_content = ectype_data["line"][line]["option"][key]["content"]
        option += f"{key}:{option_content}\n"
    option = option.rstrip('\n')
    return message.reply(content = f"""『{title}』
{content}
{option}""")

def set_ectype_state(message:Message):

    msg = message.content

    if "开启副本" in msg:
        state = "1"
        state1 = "开启"
    if "关闭副本" in msg:
        state = "0"
        state1 = "关闭"
    
    #去除消息前缀
    if "开启副本" in msg:
        msg = msg.replace("开启副本","")
    elif "关闭副本" in msg:
        msg = msg.replace("关闭副本","")
    if " " in msg :
        msg = msg.replace(" ","")

    #判断副本是否存在
    if r.get(f"ectype:{msg}") == None:
        return message.reply(content = f"副本『{msg}』不存在")
    
    r.hset("ectype:ectype",f"{msg}",state)
    return message.reply(content = f"副本『{msg}』状态修改成功（{state1}）")

