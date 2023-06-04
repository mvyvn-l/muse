from botpy.message import Message
from botpy.types.message import Embed, EmbedField

import redis
import random
import datetime
import re

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)


#摩斯密码
mos = {"A":".- ","B":"-... ","C":"-.-. ","D":"-.. ","E":". ",
        "F":"..-. ","G":"--. ","H":".... ","I":".. ","J":".--- ",
        "K":"-.- ","L":".-.. ","M":"-- ","N":"-.","O":"--- ",
        "P":".--. ","Q":"--.- ","R":".-. ","S":"... ","T":"- ",
        "U":"..- ","V":"...- ","W":".-- ","X":"-..- ","Y":"-.-- ","Z":"--.. ",
        "0":"----- ","1":".----","2":"..--- ","3":"...-- ","4":"....- ",
        "5":"..... ","6":"-.... ","7":"--... ","8":"---.. ","9":"----. "}
s="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
task_list =["占卜","浇水"]
# def task_message(message:Message):
#     now = datetime.datetime.now()
#     y=now.year
#     m=now.month
#     d=now.day
#     t=str(y)+str(m)+str(d)
#     if t == r.hget(f"task:{message.author.id}","date"):     #当日不刷新
#         pass
#     else:                                                   #次日刷新任务
#         answer=random.choice(s)
#         r.hset(f"task:{message.author.id}","date",f"{t}")
#         r.hset(f"task:{message.author.id}","message","0")

#     r.hincrby(f"task:{message.author.id}","message","1")
#     num = r.hget(f"task:{message.author.id}","message")
#     num = int(num)
#     if num % 10 == 0 and num <= 100:
#         r.zincrby("scoreboard:积分",1,f"{message.author.id}")

def message_task(message:Message):
    now = datetime.datetime.now()
    y=now.year
    m=now.month
    d=now.day
    t=str(y)+str(m)+str(d)
    if t == r.hget(f"task:{message.author.id}","date"):     #当日不刷新
        pass
    else:                                                   #次日刷新任务
        task_name = random.choice(task_list)
        r.hset(f"task:{message.author.id}","date",f"{t}")
        r.hset(f"task:{message.author.id}","message_task","0")
        r.hset(f"task:{message.author.id}","task_name",task_name)
        answer=random.choice(s)
        r.hset(f"task:{message.author.id}","topic_1",f"{mos[answer]}")
        r.hset(f"task:{message.author.id}","answer_1",f"{answer}")
        r.hset(f"task:{message.author.id}","state_1","0")
    task_name = r.hget(f"task:{message.author.id}","task_name")
    try:
        if task_name in message.content:
            r.hincrby(f"task:{message.author.id}","message_task","1")
            num = r.hget(f"task:{message.author.id}","message_task")
            num = int(num)
            if num == 1:
                r.zincrby("scoreboard:积分",10,f"{message.author.id}")
    except:
        pass

def task(message:Message):
    now = datetime.datetime.now()
    y=now.year
    m=now.month
    d=now.day
    t=str(y)+str(m)+str(d)
    print(t)
    print(now)
    
    if r.hget(f"task:{message.author.id}","state_1") == "0":    #判断任务是否完成
        state_1="未完成"
    else:
        state_1="已完成"

    ti=r.hget(f"task:{message.author.id}","topic_1")
    try:
        num = r.hget(f"task:{message.author.id}","message_task")
        task_name = r.hget(f"task:{message.author.id}","task_name")
        num = int(num)
    except:
        num = 0
    if num >= 1:
        divination = "完成"
    else:
        divination = "未完成"

    embed = Embed(
            title=f"{message.author.username}的每日任务",
            prompt="每日任务",
            fields=[
                EmbedField(name=f"任务一"),
                EmbedField(name=f"题目：{ti}"),
                EmbedField(name=f"状态：{state_1}"),
                EmbedField(name=f" "),
                EmbedField(name=f"任务二"),
                EmbedField(name=f"进行一次{task_name}(10积分) 【{divination}】"),
            ],
    )

    return message.reply(embed=embed)


def present(message:Message):
    msg=message.content
    if r.hget(f"task:{message.author.id}","state_1") == "1":
        return message.reply(content="任务一已完成")

    m=re.split("[:：]", msg)
    
    if re.search("提交任务[1一]", msg):
        topic="topic_1"
    else:
        return message.reply(content=f"<@!{message.author.id}>请输入正确的任务序号")

    if m[1] == r.hget(f"task:{message.author.id}","answer_1"):
        r.zincrby("scoreboard:积分",10,f"{message.author.id}")
        r.hset(f"task:{message.author.id}","state_1","1")
        return message.reply(content=f"""灵感者：<@!{message.author.id}>
答案：{m[1]}正确
任务一已完成，奖励10积分""")
    else:
        return message.reply(content=f"""灵感者：<@!{message.author.id}>
答案：{m[1]}错误
再接再厉""")