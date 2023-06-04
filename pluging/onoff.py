from botpy.message import Message
import redis
import re

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

#指令字典 名称-指令
commands = {"浇水":"浇水",
            "我的栀子花":"我的栀子花",
            "我的属性":"我的属性",
            "加点属性":"加点",
            "我的背包":"我的背包",
            "每日任务":"每日任务",
            "提交任务":"提交任务",
            "商城":"商城",
            "商品信息":"商品信息",
            "针对系统":"针对",
            "占卜":"占卜",
            "占卜结果":"占卜结果",
            "购买商品":"购买",
            "丢弃物品":"丢弃",
            "使用物品":"使用",
            "重置点数":"重置点数",
            "我的信息":"我的信息",
            "参加游戏":"参加游戏",
            "副本目录":"副本目录",
            "进入副本":"进入副本",
            "进行中的副本":"进行中的副本"}

for i in commands:
    #获取指令状态 1 0 None
    state = r.hget("command",f"{commands[i]}")

    #创建指令信息
    if state == None:
        r.hset("command",f"{commands[i]}",1)

def judge(message:Message):
    for i in commands:
        if message.content is not None and i in message.content:
            command = commands[i]
            state = r.hget("command",f"{command}")
            if state == "1":
                return 1
            elif state == "0":
                return 0
    
    

def set_command(message:Message):
    #开启/关闭 指令

    #匹配指令
    for i in commands:
        if i in message.content:
            command = commands[i]

    msg = message.content
    s = re.split('\s+', msg)

    if s[0] == "开启":
        state = 1
    elif s[0] == "关闭":
        state = 0
    else:
        return message.reply(content="ERROR：请正确选择开启或关闭")
    
    r.hset("command",f"{command}",f"{state}")
    return message.reply(content=f"已{s[0]}指令“{s[1]}”")

def list_command(message:Message):
    s=""
    n=0
    for i in commands:
        n+=1
        state = r.hget("command",f"{commands[i]}")
        if state == "1":
            value="开启"
        if state == "0":
            value="关闭"
        if n != 1:
            s = s + "\n"
        s = s + str(n) + " " + i + "  " +value
    
    return message.reply(content=f"{s}")