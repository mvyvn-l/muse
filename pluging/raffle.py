from botpy.message import Message

import re
import os
import redis
import random
import time
import requests

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def raffle_core(raffle_time,departure):
    if raffle_time <=10:
        p = 1
    elif raffle_time == 60:
        p = 100
    else:
        p = (raffle_time - 10) * 2
    
    if (random.random()*100 > p):
        return 2
    else:
        return 1
    
def raffle(message:Message):
