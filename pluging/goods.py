from botpy.message import Message

import redis
import re
import random

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)


def use1 (goods,num,message:Message):
    id = message.author.id
    print(r.hget(f"backpack:{id}",f"{goods}"))
    if r.hget(f"backpack:{id}",f"{goods}") == None:
        return 2
    elif int(r.hget(f"backpack:{id}",f"{goods}")) < num:
        return 3
    elif int(r.hget(f"backpack:{id}",f"{goods}")) >= num:
        return 1

def use (message:Message):
    msgs = message.content
    msg = re.split('\s+', msgs)
    id = message.author.id
    
    if len(msg) == 2:
        num = 1
    elif len(msg) == 3:
        num = int(msg[2])
    else:
        return message.reply(content = f"请检查是否有多余空格")
    
    if "精神源泉" in msg[1]:
        if "初级" in msg[1]:
            if r.hget(f"backpack:{id}",f"精神源泉•初级") == None:
                return message.reply(content = "请先购买“精神源泉•初级”")
            elif int(r.hget(f"backpack:{id}",f"精神源泉•初级")) < num:
                return message.reply(content = "所需“精神源泉•初级”不足")
            elif int(r.hget(f"backpack:{id}",f"精神源泉•初级")) >= num:
                精神源泉初级(id,num)
                return message.reply(content = f"已使用“精神源泉•初级”，恢复了{num * 1000}点精神力")

    if "灵感源泉" in msg[1]:
        if "初级" in msg[1]:
            if r.hget(f"backpack:{id}",f"灵感源泉•初级") == None:
                return message.reply(content = "请先购买“灵感源泉•初级”")
            elif int(r.hget(f"backpack:{id}",f"灵感源泉•初级")) < num:
                return message.reply(content = "所需“灵感源泉•初级”不足")
            elif int(r.hget(f"backpack:{id}",f"灵感源泉•初级")) >= num:
                灵感源泉初级(id,num)
                return message.reply(content = f"已使用“灵感源泉•初级”，恢复了{num * 1000}点灵感能量")
    
    if "核弹" in msg[1]:
        goods = "核弹"
        is_use = use1(goods,num,message)
        if is_use == 2:
            return message.reply(content = f"请先购买“{goods}”")
        if is_use == 3:
            return message.reply(content = f"所需“{goods}”不足")
        if is_use == 1:
            核弹(id,num)
            return message.reply(content = f"已使用“核弹”")
    
    if "某人的论文" in msg[1]:
        goods = "某人的论文"
        is_use = use1(goods,num,message)
        if is_use == 2:
            return message.reply(content = f"请先购买“{goods}”")
        if is_use == 3:
            return message.reply(content = f"所需“{goods}”不足")
        if is_use == 1:
            某人的论文(id,num)
            return message.reply(content = f"已使用“某人的论文”")
        
    if "咕咕鸟的羽毛" in msg[1]:
        goods = "咕咕鸟的羽毛"
        is_use = use1(goods,num,message)
        if is_use == 2:
            return message.reply(content = f"请先购买“{goods}”")
        if is_use == 3:
            return message.reply(content = f"所需“{goods}”不足")
        if is_use == 1:
            咕咕鸟的羽毛(id,num)
            return message.reply(content = f"已使用“咕咕鸟的羽毛”")
    
    if "某人的饭菜" in msg[1]:
        goods = "某人的饭菜"
        is_use = use1(goods,num,message)
        if is_use == 2:
            return message.reply(content = f"请先购买“{goods}”")
        if is_use == 3:
            return message.reply(content = f"所需“{goods}”不足")
        if is_use == 1:
            某人的饭菜(id,num)
            return message.reply(content = f"已使用“某人的饭菜”")
        
    if "某人的枕头" in msg[1]:
        goods = "某人的枕头"
        is_use = use1(goods,num,message)
        if is_use == 2:
            return message.reply(content = f"请先购买“{goods}”")
        if is_use == 3:
            return message.reply(content = f"所需“{goods}”不足")
        if is_use == 1:
            某人的枕头(id,num)
            return message.reply(content = f"已使用“某人的枕头”")

    if "城主的电脑碎片" in msg[1]:
        goods = "城主的电脑碎片"
        is_use = use1(goods,num,message)
        if is_use == 2:
            return message.reply(content = f"请先购买“{goods}”")
        if is_use == 3:
            return message.reply(content = f"所需“{goods}”不足")
        if is_use == 1:
            城主的电脑碎片(id,num)
            return message.reply(content = f"已使用“城主的电脑碎片”")
        
    if "嗑学家的粮" in msg[1]:
        goods = "嗑学家的粮"
        is_use = use1(goods,num,message)
        if is_use == 2:
            return message.reply(content = f"请先购买“{goods}”")
        if is_use == 3:
            return message.reply(content = f"所需“{goods}”不足")
        if is_use == 1:
            嗑学家的粮(id,num)
            return message.reply(content = f"已使用“嗑学家的粮”")
        
    if "水润的梨子" in msg[1]:
        goods = "水润的梨子"
        is_use = use1(goods,num,message)
        if is_use == 2:
            return message.reply(content = f"请先购买“{goods}”")
        if is_use == 3:
            return message.reply(content = f"所需“{goods}”不足")
        if is_use == 1:
            水润的梨子(id,num)
            return message.reply(content = f"已使用“水润的梨子”")

def 精神源泉初级(id,num):
    n = num * 1000
    r.hincrby(f"Character_Attribute:{id}","精神力",f"{n}")
    r.hincrby(f"backpack:{id}",f"精神源泉•初级",-num)

def 灵感源泉初级(id,num):
    n = num * 1000
    r.hincrby(f"Character_Attribute:{id}","灵感能源",f"{n}")
    r.hincrby(f"backpack:{id}",f"灵感源泉•初级",-num)

def 核弹(id,n):
    r.hincrby(f"Character_Attribute:{id}","力量",f"{n}")
    r.hincrby(f"backpack:{id}",f"核弹",-n)

def 某人的论文(id,n):
    r.hincrby(f"Character_Attribute:{id}","智慧",f"{n}")
    r.hincrby(f"backpack:{id}",f"某人的论文",-n)

def 咕咕鸟的羽毛(id,n):
    r.hincrby(f"Character_Attribute:{id}","敏捷",f"{n}")
    r.hincrby(f"backpack:{id}",f"咕咕鸟的羽毛",-n)

def 某人的饭菜(id,n):
    r.hincrby(f"Character_Attribute:{id}","意志",f"{n}")
    r.hincrby(f"backpack:{id}",f"某人的饭菜",-n)
    
def 某人的枕头(id,n):
    r.hincrby(f"Character_Attribute:{id}","体质",f"{n}")
    r.hincrby(f"backpack:{id}",f"某人的枕头",-n)
        
def 城主的电脑碎片(id,n):
    r.hincrby(f"Character_Attribute:{id}","城府",f"{n}")
    r.hincrby(f"backpack:{id}",f"城主的电脑碎片",-n)

def 嗑学家的粮(id,n):
    r.hincrby(f"Character_Attribute:{id}","外貌",f"{n}")
    r.hincrby(f"backpack:{id}",f"嗑学家的粮",-n)
        
def 水润的梨子(id,n):
    attribute_list = ["力量","智慧","敏捷","意志","体质","城府","幸运"]
    i = 1
    while i <= n:
        attribute = random.choice(attribute_list)
        r.hincrby(f"Character_Attribute:{id}",attribute,f"{1}")
        i += 1
    r.hincrby(f"backpack:{id}",f"水润的梨子",-n)