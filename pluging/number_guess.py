from botpy.message import Message

import random
import redis
import math
import re

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def join_game(message:Message,self):
    #参与游戏 1 100
    msg = message.content
    s = re.split('\s+', msg)
    id = message.author.id
    limit_max = r.hget(f"number_guess:{s[1]}","limit_max")
    score = r.zscore("scoreboard:积分", f"{message.author.id}")

    if r.hget(f"number_guess:{s[1]}","state") == None:
        return message.reply(content = f"场次{s[1]}不存在")
    if r.hget(f"number_guess:{s[1]}",f"{id}") != None:
        return message.reply(content = f"您已参加本场游戏")
    
    if score == None or int(score) < 1:
            return message.reply(content=f"{message.author.username}没有足够的积分参与游戏")
    
    if int(s[2]) <= 0 or int(s[2]) > int(limit_max):
        return message.reply(content = f"输入数字范围不正确，区间为：1~{limit_max}")

    r.hset(f"number_guess:{s[1]}",f"{id}",f"{s[2]}")
    r.hincrby(f"number_guess:{s[1]}","count","1")
    r.zincrby("scoreboard:积分",-1,f"{id}")

    return message.reply(content=f"成功使用一积分参与本场游戏")

def start_game(message:Message):
    limit_max = random.randint(100,1000)
    rate = random.randint(3,7)
    rate = rate/10
    if r.get(f"number_guess:count") == None:
        r.set("number_guess:count","0")
    else:
        r.incr("number_guess:count", amount=1)

    count = r.get(f"number_guess:count")
    r.hset(f"number_guess:{count}","state","1")
    r.hset(f"number_guess:{count}","count","0")
    r.hset(f"number_guess:{count}","limit_max",f"{limit_max}")
    r.hset(f"number_guess:{count}","rate",f"{rate}")

    return message.reply(content = f"""序列博弈
成功创建游戏
游戏序列号：{count}
数字范围：1~{limit_max}
数字倍率：{rate}
规则：私信MUSE发送 “参加游戏 {count} 所猜数字” 参与游戏，参与游戏花费1积分，积分总和将会奖励给与所有数字平均数的{rate}倍最接近的灵感者""")

def over_game(message:Message):
    msg = message.content
    s = re.split('\s+', msg)
    count = r.hget(f"number_guess:{s[1]}","count")
    rate = r.hget(f"number_guess:{s[1]}","rate")

    if r.hget(f"number_guess:{s[1]}","state") == None:
        return message.reply(content = f"场次{s[1]}不存在")
    if r.hget(f"number_guess:{s[1]}","state") == "0":
        return message.reply(content = f"场次{s[1]}已结束")
    
    r.hset(f"number_guess:{s[1]}","state","0") 

    hash_list = r.hgetall(f"number_guess:{s[1]}")
    num = 0 
    #求和
    for i in hash_list:
        if i in "state count limit_max rate":
            print (i)
        else:
            num += int(r.hget(f"number_guess:{s[1]}",f"{i}"))

    #答案
    mean_num = int(num) / int(count) * float(rate)
    mean_num = int(mean_num)
    

    min_diff = None
    nearest_keys = []
    for i in hash_list:
        if i in "state count limit_max rate":
            continue
        else:
            x = int(r.hget(f"number_guess:{s[1]}",f"{i}"))
        diff = abs(mean_num - x)
        if min_diff is None or diff < min_diff:
            min_diff = diff
            nearest_keys = [i]
        elif diff == min_diff:
            
            nearest_keys.append(i)

    win_num = len(nearest_keys)             #获胜人数
    win_score = math.floor(int(count)/int(win_num))  #获胜积分

    win_s = ""
    for id in nearest_keys:
        r.zincrby("scoreboard:积分",win_score,f"{id}")
        win_s += f"<@!{id}>"
    return message.reply(content = f"""序列博弈 {s[1]}
状态：结束
获奖用户：{win_s}
奖励积分：{win_score}
答案：{mean_num}""")