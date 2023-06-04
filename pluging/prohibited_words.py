from botpy.message import Message
import requests
import redis
import re

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def add_prohibited_words(message:Message):
    msg = message.content
    words = re.split(r'\s+', msg)

    for word in words:
        if word == "添加违禁词":
            pass
        else:
            r.sadd("prohibited_words",f"{word}")

    return message.reply(content = f"已添加违禁词")

def del_prohibited_words(message:Message):
    msg = message.content
    words = re.split(r'\s+', msg)

    for word in words:
        if word == "删除违禁词":
            pass
        else:
            r.srem("prohibited_words",f"{word}")

    return message.reply(content = f"已删除违禁词")

def detect_prohibited_words(message:Message):
    words = r.smembers("prohibited_words")
    for word in words:
        pattern = re.compile(rf'{word}', re.IGNORECASE)
        if pattern.search(message.content):
            print(pattern.search(message.content))
            return True
    '''
    url = "https://api.wer.plus/api/min"
    params = {"t": message.content}
    response = requests.get(url, params=params)
    a = ( response.json()["num"])
    if a != 0:
        return True
    '''
    
    return False
