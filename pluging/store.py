from botpy.message import Message

import redis
import re

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

level1 = {"0":"S","1":"A","2":"B","3":"C","4":"D","5":"E",} #数字转级别
level2 = {"S":"0","A":"1","B":"2","C":"3","D":"4","E":"5",} #级别转数字

#store_list:物品:0/1
#store:物品:属性：数值

def store_reload():
    if r.hget(f"store_list","精神源泉•初级") == None:
        r.hset("store_list",f"精神源泉•初级",0)
        r.hset(f"store:精神源泉•初级","数量",-1)
        r.hset(f"store:精神源泉•初级","价格",66)
        r.hset(f"store:精神源泉•初级","限购",-1)
        r.hset(f"store:精神源泉•初级","级别","E")
        r.hset(f"store:精神源泉•初级","商品介绍","""潺潺流水，沁人心肺
使用可获得1000点精神力加成""")
    
    if r.hget(f"store_list","灵感源泉•初级") == None:
        r.hset("store_list",f"灵感源泉•初级",0)
        r.hset(f"store:灵感源泉•初级","数量",-1)
        r.hset(f"store:灵感源泉•初级","价格",66)
        r.hset(f"store:灵感源泉•初级","限购",-1)
        r.hset(f"store:灵感源泉•初级","级别","E")
        r.hset(f"store:灵感源泉•初级","商品介绍","""风起柳絮，立在山巅
使用可获得1000点灵感能源加成""")
        
    if r.hget(f"store_list","核弹") == None:
        r.hset("store_list",f"核弹",0)
        r.hset(f"store:核弹","数量",-1)
        r.hset(f"store:核弹","价格",50)
        r.hset(f"store:核弹","限购",-1)
        r.hset(f"store:核弹","级别","E")
        r.hset(f"store:核弹","商品介绍","""咦，黑黝黝的丸子。
使用可获得力量点+1""")
        
    if r.hget(f"store_list","某人的论文") == None:
        r.hset("store_list",f"某人的论文",0)
        r.hset(f"store:某人的论文","数量",-1)
        r.hset(f"store:某人的论文","价格",50)
        r.hset(f"store:某人的论文","限购",-1)
        r.hset(f"store:某人的论文","级别","E")
        r.hset(f"store:某人的论文","商品介绍","""快跑，她要骂人了！
使用可获得智慧点+1""")
        
    if r.hget(f"store_list","咕咕鸟的羽毛") == None:
        r.hset("store_list",f"咕咕鸟的羽毛",0)
        r.hset(f"store:咕咕鸟的羽毛","数量",-1)
        r.hset(f"store:咕咕鸟的羽毛","价格",50)
        r.hset(f"store:咕咕鸟的羽毛","限购",-1)
        r.hset(f"store:咕咕鸟的羽毛","级别","E")
        r.hset(f"store:咕咕鸟的羽毛","商品介绍","""咕咕！咕咕咕咕！
使用可获得敏捷点+1""")

    if r.hget(f"store_list","某人的饭菜") == None:
        r.hset("store_list",f"某人的饭菜",0)
        r.hset(f"store:某人的饭菜","数量",-1)
        r.hset(f"store:某人的饭菜","价格",50)
        r.hset(f"store:某人的饭菜","限购",-1)
        r.hset(f"store:某人的饭菜","级别","E")
        r.hset(f"store:某人的饭菜","商品介绍","""呃，奇怪的颜色..
使用可获得意志点+1""")

    if r.hget(f"store_list","某人的枕头") == None:
        r.hset("store_list",f"某人的枕头",0)
        r.hset(f"store:某人的枕头","数量",-1)
        r.hset(f"store:某人的枕头","价格",50)
        r.hset(f"store:某人的枕头","限购",-1)
        r.hset(f"store:某人的枕头","级别","E")
        r.hset(f"store:某人的枕头","商品介绍","""是谁爱睡觉我不说。
使用可获得体质点+1""")
        
    if r.hget(f"store_list","城主的电脑碎片") == None:
        r.hset("store_list",f"城主的电脑碎片",0)
        r.hset(f"store:城主的电脑碎片","数量",-1)
        r.hset(f"store:城主的电脑碎片","价格",50)
        r.hset(f"store:城主的电脑碎片","限购",-1)
        r.hset(f"store:城主的电脑碎片","级别","E")
        r.hset(f"store:城主的电脑碎片","商品介绍","""是谁炸了系统厅！
使用可获得城府点+1""")
        
    if r.hget(f"store_list","嗑学家的粮") == None:
        r.hset("store_list",f"嗑学家的粮",0)
        r.hset(f"store:嗑学家的粮","数量",-1)
        r.hset(f"store:嗑学家的粮","价格",50)
        r.hset(f"store:嗑学家的粮","限购",-1)
        r.hset(f"store:嗑学家的粮","级别","E")
        r.hset(f"store:嗑学家的粮","商品介绍","""营养均衡美美哒！
使用可获得外貌点+1""")
        
    if r.hget(f"store_list","水润的梨子") == None:
        r.hset("store_list",f"水润的梨子",0)
        r.hset(f"store:水润的梨子","数量",-1)
        r.hset(f"store:水润的梨子","价格",55)
        r.hset(f"store:水润的梨子","限购",-1)
        r.hset(f"store:水润的梨子","级别","E")
        r.hset(f"store:水润的梨子","商品介绍","""一口吃掉好几个！
使用可随机增加1点数
听说有人抽出过幸运诶""")
        

def new_goods(message:Message):
    msg = message.content
    s=re.split('\s+', msg)
    msg=message.content
    state = r.hget("store_list",f"{s[1]}")
    print(1)
    print(state)
    if "创建 " in msg and state == None:
        print(2)
        r.hset("store_list",f"{s[1]}",0)
        r.hset(f"store:{s[1]}","数量",-1)
        r.hset(f"store:{s[1]}","价格",-1)
        r.hset(f"store:{s[1]}","限购",-1)
        r.hset(f"store:{s[1]}","级别","E")
        r.hset(f"store:{s[1]}","商品介绍","无")
        return message.reply(content=f"成功创建商品「{s[1]}」")
    elif "创建商品 " in msg and state != None:
        return message.reply(content=f"已存在商品「{s[1]}」")
    elif "上架商品" in msg and state != None:
        r.hset("store_list",f"{s[1]}",1)
        return message.reply(content=f"成功上架商品「{s[1]}」")
    elif "下架商品" in msg and state != None:
        r.hset("store_list",f"{s[1]}",0)
        return message.reply(content=f"成功下架商品「{s[1]}」")
    elif "上架商品" in msg and state == None:
        return message.reply(content=f"请先创建商品")
    elif "下架商品" in msg and state == None:
        return message.reply(content=f"请先创建商品")

def set_store(message:Message):
    #设置 物品 属性 数值
    
    msg=message.content
    s=re.split('\s+', msg)
    if r.hget("store_list",f"{s[1]}") == None:
        return message.reply(content="商品不存在，请先创建商品")

    if s[2] == "数量":
        if s[3].isdigit() == 0:
            return message.reply(content=f"ERROR：{s[2]}为只能为数字")
        r.hset(f"store:{s[1]}",f"{s[2]}",s[3])
        return message.reply(content=f"已设置{s[1]}的{s[2]}为{s[3]}")
    elif s[2] == "价格":
        if s[3].isdigit() == 0:
            return message.reply(content=f"ERROR：{s[2]}为只能为数字")
        r.hset(f"store:{s[1]}",f"{s[2]}",s[3])
        return message.reply(content=f"已设置{s[1]}的{s[2]}为{s[3]}")
    elif s[2] == "限购":
        if s[3].isdigit() == 0:
            return message.reply(content=f"ERROR：{s[2]}为只能为数字")
        r.hset(f"store:{s[1]}",f"{s[2]}",s[3])
        return message.reply(content=f"已设置{s[1]}的{s[2]}为{s[3]}")
    elif s[2] == "商品介绍":
        r.hset(f"store:{s[1]}",f"{s[2]}",s[3])
        return message.reply(content=f"已设置{s[1]}的{s[2]}为{s[3]}")
    elif s[2] == "级别":
        if level2[s[3]] != None:
            r.hset(f"store:{s[1]}",f"{s[2]}",s[3])
            return message.reply(content=f"已设置{s[1]}的{s[2]}为{s[3]}")
        else:
            return message.reply(content="ERROR：级别类型错误")
    else:
        return message.reply(content="ERROR：当前属性名不存在，请检查后重试")
    
def store(message:Message):

    store_reload()

    store = r.hgetall("store_list")
    s=""
    a=0
    b=0
    for key in store:
        a+=1
        if store[key] == "1":
            b+=1
            if b != 1:
                s += "\n"
            s = s + str(b) + " " + key

    return message.reply(content=f"{s}")

def store_list(message:Message):

    store_reload()

    store = r.hgetall("store_list")
    s=""
    a=0
    for key in store:
        a+=1
        if store[key] == "1":
            state = "上架"
        else:
            state = "下架"
        if a != 1:
            s += "\n"
        s = s + f"{a} {key} [{state}]"

    return message.reply(content=f"{s}")

def commodity_information(message:Message):
    #商品信息 [商品]
    msg = message.content
    msg = re.split('\s+', msg)
    if r.hget("store_list",f"{msg[1]}") == None:
        return message.reply(content="所查询商品不存在")
    s = ""
    commodity = r.hgetall(f"store:{msg[1]}")
    a=0

    if r.hget(f"store:{msg[1]}","数量") == "-1":
        num = "无限"
    else:
        num = r.hget(f"store:{msg[1]}","数量")

    if r.hget(f"store:{msg[1]}","价格") == "-1":
        price = "无价"
    else:
        price = r.hget(f"store:{msg[1]}","价格")

    if r.hget(f"store:{msg[1]}","限购") == "-1":
        limit = "不限"
    else:
        limit = r.hget(f"store:{msg[1]}","限购")

    cla = r.hget(f"store:{msg[1]}","级别")
    introduce = r.hget(f"store:{msg[1]}","商品介绍")

    s += f"商品名称：{msg[1]}" + "\n"
    s += f"数量：{num}" + "\n"
    s += f"价格：{price}" + "\n"
    s += f"限购：{limit}" + "\n"
    s += f"级别：{cla}" + "\n"
    s += f"商品介绍：{introduce}"
    
    return message.reply(content=f"{s}")
