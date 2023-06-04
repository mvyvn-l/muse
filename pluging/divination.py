from botpy.message import Message

from PIL import Image, ImageDraw, ImageFont, ImageOps
import matplotlib.backends.backend_agg as agg

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from io import BytesIO

import re
import os
import redis
import random
import time
import requests

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)


tarot=["愚者","魔法师","女祭司","皇后","皇帝",
       "教皇","恋人","战车","力量","隐者",
       "命运之轮","正义","倒吊者","死神","节制",
       "恶魔","高塔","星星","月亮","太阳",
       "审判","世界","空白"]

p=["自由、活在当下、愚蠢、癫狂、放纵、陶醉、精神错乱、狂热、泄漏、无知、毫无经验、盲目行动、冒险、从零开始、进入全新的环境、不拘形式的自由恋爱、不按常理出牌。",
    "事情的开始，行动的改变，熟练的技术及技巧，贯彻我的意志，运用自然的力量来达到野心。",
    "开发出内在的神秘潜力，前途将有所变化的预言，深刻的思考，敏锐的洞察力，准确的直觉。",
    "幸福，成功，收获，无忧无虑，圆满的家庭生活，良好的环境，美貌，艺术，与大自然接触，愉快的旅行，休闲。",
    "光荣，权力，胜利，握有领导权，坚强的意志，达成目标，父亲的责任，精神上的孤单。",
    "援助，同情，宽宏大量，可信任的人给予的劝告，良好的商量对象，得到精神上的满足，遵守规则，志愿者。",
    "撮合，爱情，流行，兴趣，充满希望的未来，魅力，增加朋友。感情和肉体对爱的渴望，它暗示恋情将向彼此关系更亲密的方向发展。事业上将面临重大的抉择，它将关系到你的未来前途。",
    "努力而获得成功，胜利，克服障碍，行动力，自立，尝试，自我主张，年轻男子，交通工具，旅行运大吉。",
    "大胆的行动，有勇气的决断，新发展，大转机，异动，以意志力战胜困难，健壮的女人。",
    "隐藏的事实，个别的行动，倾听他人的意见，享受孤独，自己的丢化，有益的警戒，年长者，避开危险，祖父，乡间生活。",
    "关键性的事件，有新的机会，因的潮流，环境的变化，幸运的开端，状况好转，问题解决，幸运之神降临。命运之轮正转到了你人生最低迷的时刻，也许你有些无法接受，但是若能以平常心来看待，这无疑是你成长的最好时机，需要认真面对。感情方面所受到的挫折近乎让你崩溃，然而你还在不断努力。虽然你面前是无数的荆棘，但坚持过去将是平坦的大道。你会发现以前所付出的无谓努力，而今反而成了你前进的动力，先前的付出终于有了回报。命运之轮是由命运女神转动的，所以你俩之前的风风雨雨都将过去，关系将进入稳定的发展阶段。",
    "公正、中立、诚实、心胸坦荡、表里如一、身兼二职、追求合理化、协调者、与法律有关、光明正大的交往、感情和睦。",
    "接受考验、行动受限、牺牲、不畏艰辛、不受利诱、有失必有得、吸取经验教训、浴火重生、广泛学习、奉献的爱。当牌面正立时，你的事业会有短暂的停顿，但你很清楚其中的原因，再次确认自己的目标，做好出发的准备。感情上同样需要反省的时间，你对爱情的牺牲对会给对方很大的触动，也会成为你们关系发展的催化剂。",
    "失败、接近毁灭、生病、失业、维持停滞状态、持续的损害、交易停止、枯燥的生活、别离、重新开始、双方有很深的鸿沟、恋情终止。事业上你将放弃一些得到的利益，并获得全新的发展机会。在感情上，你将会发生深刻的变化，将开始新的阶段，接受事实你们会有更加美好的旅程。",
    "单纯、调整、平顺、互惠互利、好感转为爱意、纯爱、深爱。你在事业上小心翼翼，因为处事理智让你的同事感到十分放心。当下你们的感情简简单单，一切都是这么的单纯、平静，正是因为彼此的沟通才让这段感情之路如此通畅。",
    "被束缚、堕落、生病、恶意、屈服、欲望的俘虏、不可抗拒的诱惑、颓废的生活、举债度日、不可告人的秘密、私密恋情。你将在事业中得到相当大的名声与财富，你心中的事业就是一切，财富就是你的目标。感情上你们开始被彼此束缚，却不希望改善这种关系，情愿忍受彼此的牵连和不满。",
    "破产、逆境、被开除、急病、致命的打击、巨大的变动、受牵连、信念崩溃、玩火自焚、纷扰不断、突然分离，破灭的爱。事业上的困难显而易见，回避不是办法，要勇于挑战，尽管它貌似强大。在感情方面，突然的改变让你陷入深深的痛苦中，接受改变可以让你或你们双方在未来的人生旅途中走得更好。",
    "前途光明、充满希望、想象力、创造力、幻想、满足愿望、水准提高、理想的对象、美好的恋情。代表当你在事业上得到希望的能量时，前途会无比光明。在感情方面，你对自己很有信心，对两人的关系也抱有乐观的态度，相信自己能把握主动权，并努力追求对方，你们很可能就是命中注定的那一对。",
    "不安、迷惑、动摇、谎言、欺骗、鬼迷心窍、动荡的爱、三角关系。在事业上，你可能有些不满足，希望能够把自己内在的力量全使出来，于是你开始想要晚上的时间。感情方面，你很敏感害怕被伤害，尽管有伴侣的承诺，你仍然犹豫不决，甚至有逃避的想法。",
    "活跃、丰富的生命力、充满生机、精力充沛、工作顺利、贵人相助、幸福的婚姻、健康的交际。事业上会有贵人相助，将会有更好的发展机遇。在感情方面，你们已经走出坎坷的感情之路，前面将是洒满歌声和欢乐的坦途，你们将开始规划未来的生活。",
    "复活的喜悦、康复、坦白、好消息、好运气、初露锋芒、复苏的爱、重逢、爱的奇迹。当牌面正立时，事业上你超越了自我，在过去努力的基础上取得了成功。感情上双方都在认真学习和成长，虽然表面上的变化并不大，但内在的改变已经很大了。",
    "完成、成功、完美无缺、连续不断、精神亢奋、拥有毕生奋斗的目标、完成使命、幸运降临、快乐的结束、模范情侣。在事业上因为努力工作，所以回报丰厚。感情上，你们在彼此的承诺中持续着美好的关系。",
    "看不透你呢，但似乎是好事"
    ]
n=["粗心大意、缺席、分散、漫不经心、冷淡、微不足道、虚荣、不负责任、感情轻浮、失去纯真、缺乏责任心、破碎、漂泊不定、不守规矩、无法听从内心的本能行事、过度小心错失良机。",
   "意志力薄弱，起头难，走入错误的方向，知识不足，被骗和失败。",
    "过于洁癖，无知，贪心，目光短浅，自尊心过高，偏差的判断，有勇无谋，自命不凡。",
    "不活泼，缺乏上进心，散漫的生活习惯，无法解决的事情，不能看到成果，耽于享乐，环境险恶，与家人发生纠纷。",
    "幼稚，无力，独裁，撒娇任性，平凡，没有自信，行动力不足，意志薄弱，被支配。",
    "错误的讯息，恶意的规劝，上当，援助被中断，愿望无法达成，被人利用，被放弃。",
    "禁不起诱惑，纵欲过度，反覆无常，友情变淡，厌倦，争吵，华丽的打扮，优柔寡断。感情上表现幼稚，对成长虽有期待与希望，却希望永远躲避危险，逃避责任。事业上总保持着很高的戒心，让人感到很不舒服，不愿同你合作。",
    "争论失败，发生纠纷，阻滞，违返规则，诉诸暴力，顽固的男子，突然的失败，不良少年，挫折和自私自利。",
    "胆小，输给强者，经不起诱惑，屈服在权威与常识之下，没有实践便告放弃，虚荣，懦弱，没有耐性。内心的恐惧使你畏首畏尾，进而遭遇事业的瓶颈，感到失去了自信。在爱情上患得患失，失去清醒的判断。",
    "无视警，憎恨孤独，自卑，担心，幼稚思想，过于慎重导致失败，偏差，不宜旅行。在事业中过多的投入已经让你不愿面对其它事情，因而事业有了突破性的进展。在感情方面，用工作繁忙来逃避这段感情的发展，对伴侣态度冷淡，因为害怕感情的发展而在关键时刻退缩，使对方心寒。",
    "边疆的不行，挫折，计划泡汤，障碍，无法修正方向，往坏处发展，恶性循环，中断。",
    "失衡、偏见、纷扰、诉讼、独断专行、问心有愧、无法两全、表里不一、男女性格不合、情感波折、无视社会道德的恋情。长时间的压抑使你在事业最关键的时刻倒下了，需要认真修整一番才能再次前进。感情上你一直忍让着，然而这次你却爆发了，开始指责对方的不是，你们的感情将会有很大的波折。",
    "无谓的牺牲、骨折、厄运、不够努力、处于劣势、任性、利己主义者、缺乏耐心、受惩罚、逃避爱情、没有结果的恋情。当牌面倒立时，事业上缺乏远见，迷失了努力的目标。感情上你没有了为对方付出的念头，而对方对你的态度依旧，这使你更想逃避。你已经忽略了内心深处正确的判断力，这让你开始遇到很多失败。",
    "抱有一线希望、起死回生、回心转意、摆脱低迷状态、挽回名誉、身体康复、突然改变计划、逃避现实、斩断情丝、与旧情人相逢。事业上你在试图“两全其美”，希望能够发生奇迹。在感情上，对方已经接受了改变，而你却在逃避现实，你俩的距离正在越来越大。",
    "消耗、下降、疲劳、损失、不安、不融洽、爱情的配合度不佳。在事业上，你陷入了朝令夕改的怪圈，不妨效仿一下愚人勇往直前，或许能够取得更大的成功。感情上彼此虽然还在不断尝试着沟通，但每次之后总是感觉没有收获，正因为如此你们之间的距离才会越拉越大。",
    "逃离拘束、解除困扰、治愈病痛、告别过去、暂停、别离、拒绝诱惑、舍弃私欲、别离时刻、爱恨交加的恋情。事业上理性开始支配欲望，找到真正值得努力的目标。感情上开始尝试与对方进行沟通，这让你俩的感情更加牢固。",
    "困境、内讧、紧迫的状态、状况不佳、趋于稳定、骄傲自大将付出代价、背水一战、分离的预感、爱情危机。事业上开始有稳定的迹象，你不要盲目抵抗改变的发生，这只会导致更大的改变，无论你如何抵抗，改变终究会发生。在感情上双方的情绪终于平静下来，虽然沟通上还有些困难，但不会有太大的变化了，也许你做些让步，会让你们的感情更融洽。",
    "挫折、失望、好高骛远、异想天开、仓皇失措、事与愿违、工作不顺心、情况悲观、秘密恋情、缺少爱的生活。在事业上，你不要全部依靠别人的给予，因为你还有希望在心中燃烧，只有靠自己才有真正的发展动力。感情方面你俩无法彼此信任，感觉无法把自己托付给对方，也许你们退一步，都冷静一下就能找出解决问题的途径，因为答案就在你们的心中。",
    "逃脱骗局、解除误会、状况好转、预知危险、等待、正视爱情的裂缝。在事业上，你因为外界的压力开始退缩了，并对自己的既定目标产生了怀疑。在感情上，你们之间的问题开始浮现，虽然有些痛，但是只要共同面对存在的困难，问题就解决一半了。",
    "消沉、体力不佳、缺乏连续性、意气消沉、生活不安、人际关系不好、感情波动、离婚。事业上竞争心太急切了，把对手都吓跑了，然而也让合作伙伴感到害怕，或许你该放松些。感情上两人间出现一些小变化，开始在乎对方的态度和自己的付出，这些怀疑也许都是没必要的。",
    "一蹶不振、幻灭、隐瞒、坏消息、无法决定、缺少目标、没有进展、消除、恋恋不舍。在事业上缺乏清晰的判断，试图用物质填充精神的空虚。在感情上，不断地回忆着过去的美好时光，不愿意去正视眼前的问题，你们的关系已经是貌合神离了。",
    "未完成、失败、准备不足、盲目接受、一时不顺利、半途而废、精神颓废、饱和状态、合谋、态度不够融洽、感情受挫。在事业的路上有巨大的障碍，你精神不振，丧失了挑战的动力。感情上，你们不再重视承诺，只是盲目接受对方。彼此最好能沟通一下，不要让痛苦继续纠缠着你们。",
    "看不透你呢，但今天要小心哦",
]

url = [
    "https://pic2.imgdb.cn/item/64570e480d2dde5777d180c6.webp",
    "https://pic2.imgdb.cn/item/64570e480d2dde5777d180ee.webp",
    "https://pic2.imgdb.cn/item/64570e480d2dde5777d18114.webp",
    "https://pic2.imgdb.cn/item/64570e490d2dde5777d18145.webp",
    "https://pic2.imgdb.cn/item/64570e490d2dde5777d1818a.webp",
    "https://pic2.imgdb.cn/item/64570e510d2dde5777d19693.webp",
    "https://pic2.imgdb.cn/item/64570e520d2dde5777d1972e.webp",
    "https://pic2.imgdb.cn/item/64570e520d2dde5777d197bc.webp",
    "https://pic2.imgdb.cn/item/64570e510d2dde5777d1954f.webp",
    "https://pic2.imgdb.cn/item/64570e510d2dde5777d1960a.webp",
    "https://pic2.imgdb.cn/item/64570e570d2dde5777d1a7e3.webp",
    "https://pic2.imgdb.cn/item/64570e580d2dde5777d1a804.webp",
    "https://pic2.imgdb.cn/item/64570e580d2dde5777d1a844.webp",
    "https://pic2.imgdb.cn/item/64570e580d2dde5777d1a86d.webp",
    "https://pic2.imgdb.cn/item/64570e580d2dde5777d1a8ab.webp",
    "https://pic2.imgdb.cn/item/64570e5f0d2dde5777d1af18.webp",
    "https://pic2.imgdb.cn/item/64570e5e0d2dde5777d1ae23.webp",
    "https://pic2.imgdb.cn/item/64570e5e0d2dde5777d1ae57.webp",
    "https://pic2.imgdb.cn/item/64570e5e0d2dde5777d1aeae.webp",
    "https://pic2.imgdb.cn/item/64570e5f0d2dde5777d1aed6.webp",
    "https://pic2.imgdb.cn/item/64570e6d0d2dde5777d1b86e.webp",
    "https://pic2.imgdb.cn/item/64570e6e0d2dde5777d1b8b6.webp",
    "https://pic2.imgdb.cn/item/64570e6e0d2dde5777d1b925.webp",
]
def divination(message:Message,a):
    
    x = random.randint(0,22)
    Positive_or_negative =random.randint(0,100)
    user_id = message.author.id
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))  #获取日期
    day= f"divination:{user_id}:{today}"      #日期
    serial= f"divination:{user_id}:serial"    #牌号
    pon = f"divination:{user_id}:pon"         #正逆 正-1  逆-0
    score = r.zscore("scoreboard:积分", f"{message.author.id}")
    img_url = url[x]
    #打开图片
    #img=Image.open(f"pluging/star/{x} {tarot[x]}.png")  #本地
    # img=Image.open(os.path.join('/home/mvyvn/muse/pluging/star', f'{x} {tarot[x]}.png'))  #服务器路径
    img = requests.get(img_url)
    img = Image.open(BytesIO(img.content))
    if Positive_or_negative >= 40:
        P_or_n = 1
    else:
        P_or_n = 0

    if r.get(day) and a==1:
        if r.get(pon) == "1":
            pon_s = "正位"
        else:
            pon_s = "逆位"
        x = int(r.get(serial))
        return message.reply(content=f"今天已经占卜过了哦，是[{tarot[x]}] [{pon_s}]呢，明天再来吧~")

    elif r.get(day) and a==0:
        return 0
    
    elif a==1:
        if score == None or int(score) < 5:
            return message.reply(content=f"{message.author.username}没有足够的积分进行占卜")
        else:
            r.zincrby("scoreboard:积分",-5,f"{message.author.id}")
            return message.reply(content=f"{message.author.username}花费了5积分进行占卜")
        
    elif a == 0 and int(score) >= 5:
        r.set(day, today)
        r.set(serial, x)
        r.set(pon, P_or_n)
        r.expire(serial, 86400)


    #正位-逆位
    if r.get(pon) == "1":
        pon_s = "正位"
        s = p[x]
        dian = random.randint(4,10)
        msg = f"今天运气很好呢，捡到了{dian}积分"
        r.zincrby("scoreboard:积分",dian,f"{message.author.id}")
    else:
        pon_s = "逆位"
        s = n[x]
        #逆位-旋转图片180°
        img = img.rotate(180)
        dian = random.randint(3,5)
        msg = f"今天运气不是很好呀，那就奖励你{dian}积分吧"
        r.zincrby("scoreboard:积分",dian,f"{message.author.id}")


     # 将文件保存为二进制文件流
    img_bytes = BytesIO()  # 创建一个二进制对象 并将图像内容写入到二进制对象中 获得一个二进制图像文件类型
    img.save(img_bytes, format="PNG")


########################################################################################
    return message.reply(content=f"""MUSE 洞悉了{message.author.username}今日的运势

[{tarot[x]}] [{pon_s}]

释义：{s}

{msg}""",
                         file_image=img_bytes.getvalue())
########################################################################################

def divination_result(message:Message):
    user_id = message.author.id
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))  #获取日期
    day= f"divination:{user_id}:{today}"      #日期
    serial= f"divination:{user_id}:serial"    #牌号
    x = int(r.get(serial))
    pon = f"divination:{user_id}:pon"         #正逆 正-1  逆-0

    img_url = url[x]
    #打开图片
    img = requests.get(img_url)
    img = Image.open(BytesIO(img.content))

    if r.get(day):
        if r.get(pon) == "1":
            pon_s = "正位"
        else:
            pon_s = "逆位"
            #逆位-旋转图片180°
            img = img.rotate(180)
         # 将文件保存为二进制文件流
        img_bytes = BytesIO()  # 创建一个二进制对象 并将图像内容写入到二进制对象中 获得一个二进制图像文件类型
        img.save(img_bytes, format="PNG")
        return message.reply(content=f"{message.author.username}今日的运势是[{tarot[x]}] [{pon_s}]哟",file_image=img_bytes.getvalue())
    else:
        return message.reply(content=f"快来占卜让我看看{message.author.username}今日的运势吧")
    
def for_answer(message:Message):
    
    url = "https://api.wer.plus/api/bay"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()["data"]
        data = data["comment"]
        return message.reply(content = f"{data}")
    else:
        print("Error:", response.status_code)
    
def yiyan(message:Message):
    
    url = "https://v1.hitokoto.cn/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()["hitokoto"]
        data_from = response.json()["from"]
        return message.reply(content = f"""{data}
————{data_from}""")
    else:
        print("Error:", response.status_code)
    