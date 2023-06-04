from botpy.message import Message

import redis
import re

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

#权限列表
limits_list = ["测试权限",
               "给予物品",
               "权限管理",
               "商城管理",
               "指令启停",
               "针对系统",
               "违禁检测",
               "数值管理",
               "序列博弈",
               "副本系统",
               "清理成员"]


def all_limit(message:Message):
    
    a=0
    s=""
    for i in limits_list:
        a+=1
        if a!=1:
            s=s + "\n"
        s=s+f"{a}" + "「" + i + "」"
    return message.reply(content=f"{s}")

def set_limit(message:Message):

    #分割消息
    msg = message.content
    s=re.split('\s+', msg)

    #更新权限列表
    for i in limits_list:
        limit_bool = False
        if r.hget(f"limits:{i}","state") == None:
            r.hset(f"limits:{i}","state","1")
        #判断权限是否存在
        if s[1] == i:
            limit_bool = True

    
    if limit_bool == 0:
        return message.reply(content="ERROR:权限名错误，请确认后重试")


    #判断个人或者身份组
    if "身份组" in message.content:
        limit_type = "roles"
    elif "用户" in message.content:
        limit_type = "id"
    elif "身份组" in message.content or "用户" in message.content:
        return message.reply(content="ERROR:不可同时设置个人与身份组")
    else:
        return message.reply(content="ERROR:请选择个人或身份组")

    #获取要设置的用户id或身份组
    if limit_type == "roles":
        x=s[3]
    else:
        x=message.mentions[0].id

    #判断添加或撤销权限
    if "添加" in message.content:
        limit_set = 1
    elif "撤销" in message.content:
        limit_set = 0
    else:
        return message.reply(content="ERROR: 添加权限 / 撤销权限")
    
    #写入数据库
    r.hset(f"limits:{s[1]}",f"{limit_type}:{x}",f"{limit_set}")

    #回复
    return message.reply(content=f"已为{s[2]} {x} {s[0]} {s[1]}")

def is_limit(x,message:Message):

    #判断频道主或管理员
    if "4" in message.member.roles or "2" in message.member.roles:
        print("频道主/管理员")
        return 1
    
    #判断用户是否拥有权限
    elif r.hget(f"limits:{x}",f"id:{message.author.id}") == "1":
        print("已有权限用户")
        return 1
    
    #判断用户身份组是否拥有权限
    else:
        roles=message.member.roles
        for i in roles:
            if r.hget(f"limits:{x}",f"roles:{i}") == "1":
                print("已有权限身份组")
                return 1
         
    print(f"{message.author.username}没有权限")
    return 0

def test_limit(message:Message):
    return message.reply(content="SUCCESS！")