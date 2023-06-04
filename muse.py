# -*- coding: utf-8 -*-

import botpy
from botpy import logging

from botpy.message import Message
from botpy.types.announce import AnnouncesType
from botpy.ext.cog_yaml import read
from botpy.message import DirectMessage
from botpy.types.message import Embed, EmbedField
from botpy.forum import OpenThread

import redis
import re
import os
import sys
import time
from datetime import datetime
from datetime import date

from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
from io import BytesIO

from pluging.gardenia import water
from pluging.gardenia import my_gardenia
from pluging.Character_Attribute import my_Character_Attribute
from pluging.Character_Attribute import add_count
from pluging.Character_Attribute import restart
from pluging.Character_Attribute import my_information
from pluging.backpack import give
from pluging.backpack import my_backpack
from pluging.backpack import del_goods
from pluging.backpack import buy_goods
from pluging.task import task
from pluging.task import present
from pluging.task import message_task
from pluging.limits import set_limit
from pluging.limits import is_limit
from pluging.limits import test_limit
from pluging.limits import all_limit
from pluging.store import new_goods
from pluging.store import set_store
from pluging.store import store_list
from pluging.store import store
from pluging.store import commodity_information
from pluging.onoff import set_command
from pluging.onoff import list_command
from pluging.onoff import judge
from pluging.Aim_At import detection
from pluging.Aim_At import aim_at
from pluging.divination import divination
from pluging.divination import divination_result
from pluging.divination import for_answer
from pluging.divination import yiyan
from pluging.prohibited_words import add_prohibited_words
from pluging.prohibited_words import del_prohibited_words
from pluging.prohibited_words import detect_prohibited_words
from pluging.goods import use
from pluging.set_value import admin_set
from pluging.number_guess import join_game
from pluging.number_guess import start_game
from pluging.number_guess import over_game
from pluging.other import rua
from pluging.other import role_list
from pluging.email import qq_bind
from pluging.email import verify
from pluging.email import unbind

import psutil



def restart_program():  #重启程序
    python = sys.executable
    os.execl(python, python, *sys.argv)

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"「{self.robot.name}」 on_ready!")
        after_id = "0"
        for i in range(0,400):
                members = await self.api.get_guild_members("13118725095733118798",limit=400,after=after_id)
                after_id = members[-1]["user"]["id"]
                for user in members:
                        id = user["user"]["id"]
                        username = user["user"]["username"]
                        nick = user["nick"]
                        r.hset("id_name",id,username)
                        r.hset("id_nick",id,nick)



    async def on_message_create(self, message: Message):

        _log.info(f"{message.author.id}-{message.author.username}:{message.content}")
        
        msg=message.content
        msg = msg.replace("<@!1511043533148073052> ","")
        msg = msg.replace("<@!16378502700398537878>","")

        msg = msg.replace("/","")

        if "restart" == msg and "4" in message.member.roles:
            await message.reply(content = f"重启成功")
            restart_program()
        if msg == None:
            if detection(message) == "1":
                await self.api.recall_message(message.channel_id, message.id, hidetip=True)

        if judge(message)==0 and "开启 " not in msg:
            return 0
        if "针对" in msg and is_limit("针对系统",message):
            await aim_at(message)
        if "添加违禁词" in msg and is_limit("违禁检测",message):
            await add_prohibited_words(message)
        if "删除违禁词" in msg and is_limit("违禁检测",message):
            await del_prohibited_words(message)
        if detect_prohibited_words(message) == True:
            await self.api.recall_message(message.channel_id, message.id, hidetip=True)
            await message.reply(content = f"{message.author.username}触发违禁词，处理有误联系管理员")
            await self.api.mute_member(message.guild_id, message.author.id, mute_seconds="600")
        if detection(message) == "1":
            try:
                thread = await self.api.get_threads(channel_id=message.channel_id)
                tid = thread["threads"][0]["thread_info"]["thread_id"]
                uid = thread["threads"][0]["author_id"]
                if uid == message.author.id:
                    await self.api.delete_thread(channel_id=message.channel_id,thread_id=tid)
            except:
                pass
            await self.api.recall_message(message.channel_id, message.id, hidetip=True)
        if "开启 " in msg or "关闭 " in msg and is_limit("指令启停",message):
            await set_command(message)
        if "列出指令" == msg and is_limit("指令启停",message):
            await list_command(message)
        if "浇水" == msg:
            await water(message)
        if "我的栀子花" == msg:
            await my_gardenia(message)
        if "我的属性" == msg:
            await my_Character_Attribute(message)
            #await my_Character_Attribute(message,2)
        if "加点 " in msg:
            await add_count(message)
        if "我的背包" == msg:
            await my_backpack(message)
        if "给予" in message.content and is_limit("给予物品",message):
            await give(message)
        if "丢弃" in msg:
            await del_goods(message)
        if "购买" in msg:
            await buy_goods(message)
        message_task(message)
        if "每日任务" == msg:
            await task(message)
        if "提交任务" in msg:
            await present(message)
        if "权限 " in msg and is_limit("权限管理",message):
            await set_limit(message) 
        if "测试权限" == msg and is_limit("测试权限",message):
            await test_limit(message)
        if "列出权限" == msg and is_limit("权限管理",message):
            await all_limit(message)
        if "上架商品 " in msg or "下架商品 " in msg or "创建商品 " in msg and is_limit("商城管理",message):
            print(1)
            await new_goods(message)
        if "设置 " in msg and is_limit("商城管理",message):
            await set_store(message)
        if "列出商品" == msg and is_limit("商城管理",message):
            await store_list(message)
        if "商城" == msg:
            await store(message)
        if "商品信息 " in msg:
            await commodity_information(message)
        if "占卜" == msg:
            await divination(message,1)
            await divination(message,0)
        if "占卜结果" == msg:
            await divination_result(message)
        if "给我一个答案" == msg:
            await for_answer(message)
        if "一言" == msg:
            await yiyan(message)
        if "使用" in msg:
            await use(message)
        if msg == "重置点数":
            await restart(message)
        if re.match(r"^.*(添加|增加|扣除|减少).*$", msg) and "身份组" not in msg and is_limit("数值管理",message):
            await admin_set(message,0)
        if re.match(r"^.*(添加|增加|扣除|减少).*$", msg) and "身份组" in msg and is_limit("数值管理",message):
            after_id = "0"
            for i in range(0,400):
                is_end = True
                while is_end:
                    members = await self.api.get_guild_members(message.guild_id,limit=400,after=after_id)
                    try:
                        after_id = members[-1]["user"]["id"]
                    except:
                        is_end = False
                    print(members[-1]["nick"])
                    await admin_set(message,members)
        if "我的信息" == msg:
            await my_information(message)
        if "开启游戏" == msg and is_limit("序列博弈",message):
            await start_game(message)
        if "结束游戏" in msg and is_limit("序列博弈",message):
            await over_game(message)
        if "解除私信限制" == msg:
            dms = await self.api.create_dms(guild_id=message.guild_id, user_id=message.author.id)
            await self.api.post_dms(guild_id=dms["guild_id"],content=f"解除限制")
        if "rua" in msg:
            await rua(message)
        if "server_state" == msg and "4" in message.member.roles:
            # 获取CPU占用率
            cpu_percent = psutil.cpu_percent()
            # 获取内存占用率
            memory_percent = psutil.virtual_memory().percent
            await message.reply(content = f"""MUSEの小窝
CPU占用率：{cpu_percent}%
内存占用率：{memory_percent}%""")
        if "身份组列表" == msg:
            roles_list = await self.api.get_guild_roles(message.guild_id)
            await role_list(message,roles_list)
        if "clean" == msg and is_limit("清理成员",message):
            await message.reply(content = "清理中，可能需要几分钟的时间，请等待回复后进行下一步操作")
            num = 0
            after_id = "0"
            is_end = True
            while is_end:
                members = await self.api.get_guild_members(message.guild_id,limit=400,after=after_id)
                try:
                    after_id = members[-1]["user"]["id"]
                except:
                    is_end = False
                for member in members:
                    role = member["roles"]
                    is_bot = member["user"]["bot"]
                    iso_date = member["joined_at"]
                    id = member["user"]["id"]
                    dt = datetime.fromisoformat(iso_date)
                    date_part = dt.date()
                    today = date.today()
                    date_difference = (today - date_part).days
                    if "11" in role and date_difference >= 30 and is_bot == False:
                        try:
                            await self.api.get_delete_member(guild_id=message.guild_id, user_id=id, add_blacklist=False, delete_history_msg_days=0)
                        except:
                            time.sleep(21)
                            await self.api.get_delete_member(guild_id=message.guild_id, user_id=id, add_blacklist=False, delete_history_msg_days=0)
                        num += 1
                        print(member["user"]["username"],date_difference)
            await message.reply(content = f"成功清理{num}人")


        


    async def on_direct_message_create(self, message: DirectMessage):
        _log.info(f"{message.author.id}-{message.author.username}:{message.content}")
        msg = message.content
        if "参加游戏" in msg:
            await join_game(message,self)
        if "绑定QQ" in msg:
            await qq_bind(message)
        
        if "验证码" in msg:
            if verify(message,1) == 1:
                await self.api.create_guild_role_member(
                    guild_id="12129458028700690480",
                    role_id="15038693", 
                    user_id=message.author.id, 
                )
            await verify(message,0)
        if "解绑" in msg:
            if unbind(message,1) == 1:
                await self.api.delete_guild_role_member(
                    guild_id="12129458028700690480",
                    role_id="15038693", 
                    user_id=message.author.id, 
                )
            await unbind(message,0)


if __name__ == "__main__":
    
    while True:
        try:
            intents = botpy.Intents.all()
            client = MyClient(intents=intents) 
            client.run(appid=test_config["appid"], token=test_config["token"])
            break
        except Exception as e:
            time.sleep(5)
    # intents = botpy.Intents.all()
    # client = MyClient(intents=intents) 
    # client.run(appid=test_config["appid"], token=test_config["token"])
