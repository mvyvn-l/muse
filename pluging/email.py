from botpy.message import Message


import re
import redis
import random
import time
import requests

pool = redis.ConnectionPool(host='localhost', port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool)

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

html_c ="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html lang="en"><head><meta http-equiv="Content-Type" content="text/html charset=UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width,initial-scale=1"><style type="text/css">*{padding:0;margin:0}html,body{padding:0;margin:0;font-size:14px;line-height:normal;color:initial;-webkit-text-size-adjust:100%;-moz-text-size-adjust:100%;text-size-adjust:100%;font-family:Source Han Sans CN,Helvetica Neue,Helvetica,Microsoft YaHei,Arial,sans-serif !important}a{text-decoration:none !important;color:initial}p{line-height:normal;margin:0}table{border-spacing:0 !important;table-layout:fixed !important}table,td{mso-table-lspace:0pt !important}ul,ol{-webkit-padding-start:20px;padding-inline-start:20px}.py-templateWrap{background:#fff;font-size:14px;position:relative;z-index:0;overflow-wrap:break-word;word-wrap:break-word;color:#222;table-layout:fixed;border-spacing:0 !important}.py-templateWrap table{table-layout:fixed;border-spacing:0 !important}.py-templateWrap .py-shapeWrap{width:100%;table-layout:fixed}.py-templateWrap .py-shapeWrap .py-colWrap{table-layout:fixed}.py-templateWrap a{text-decoration:none !important}.py-templateWrap p{line-height:normal;margin:0}.py-templateWrap .widgetButton p{line-height:unset;line-height:inherit}@media screen and (max-width: 768px){.py-templateWrap .py-shapeWrap-mobileFit .py-colWrap{width:100% !important;display:block !important}}</style></head><body><table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" class="py-templateWrap" style="margin: 0px auto !important; width: 100% !important; overflow: hidden;"><tbody><tr><td align="center"><div class="cube hasContent"><table bgcolor="#E8E8E8" aria-hidden="true" border="0" cellpadding="0" cellspacing="0" width="100%" class="py-shapeWrap" style="max-width: 600px; margin: 0px auto; width: 100%; background-color: rgb(232, 232, 232); background-image: url(&quot;undefined&quot;); background-position: center center; background-size: cover; padding: 0px 20px;"><tbody><tr><th valign="top" class="py-colWrap" style="width: 100%; font-weight: normal; padding: 0px; text-align: initial;"><div class="cube hasContent"><table cellpadding="0" cellspacing="0" width="100%" align="center" aria-hidden="true" class="widget_1_0_0" style="width: 100% !important; padding: 10px; box-sizing: border-box; line-height: normal; font-size: 14px;"><tbody><tr><td class="Widget index-module_Widget_3Alx7" style="width: 100% !important;"><table aria-hidden="true" cellpadding="0" cellspacing="0" border="0" align="center" width="100%" class="WidgetBlank"><tbody><tr><td align="center" height="20"><table aria-hidden="true" cellpadding="0" cellspacing="0" border="0" align="center" width="100%"><tbody><tr><td></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></div><div class="cube hasContent"><table cellpadding="0" cellspacing="0" width="100%" align="center" aria-hidden="true" class="widget_1_0_1" style="width: 100% !important; padding: 10px; box-sizing: border-box; line-height: normal; font-size: 14px;"><tbody><tr><td class="Widget index-module_Widget_3Alx7" style="width: 100% !important;"><table aria-hidden="true" cellpadding="0" cellspacing="0" border="0" align="center" width="100%" class="WidgetBlank"><tbody><tr><td align="center" height="20"><table aria-hidden="true" cellpadding="0" cellspacing="0" border="0" align="center" width="100%"><tbody><tr><td></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></div><div class="cube hasContent"><table cellpadding="0" cellspacing="0" width="100%" align="center" aria-hidden="true" class="widget_1_0_2" style="width: 100% !important; padding: 10px 10px 0px; box-sizing: border-box; line-height: normal; font-size: 14px;"><tbody><tr><td class="Widget index-module_Widget_3Alx7" style="width: 100% !important;"><table cellpadding="0" cellspacing="0" border="0" width="100%" class="tinymce-wrap index-module_WidgetText_2MGea" style="font-size: 14px;"><tbody><tr><td><div><p style="margin: 0;padding: 0;text-align: center;"><span style="font-family: impact, chicago; font-size: 48px;"><strong><span style="color: #040f5b;">欢迎来到\n灵感之城</span></strong></span></p></div><div style="clear: both; display: block; width: 100%; overflow: hidden; height: 0px;"></div></td></tr></tbody></table></td></tr></tbody></table></div><div class="cube hasContent"><table cellpadding="0" cellspacing="0" width="100%" align="center" aria-hidden="true" class="widget_1_0_3" style="width: 100% !important; padding: 10px; box-sizing: border-box; line-height: normal; font-size: 14px;"><tbody><tr><td class="Widget index-module_Widget_3Alx7" style="width: 100% !important;"><table cellpadding="0" cellspacing="0" border="0" width="100%" class="tinymce-wrap index-module_WidgetText_2MGea" style="font-size: 14px;"><tbody><tr><td><div></div><div style="clear: both; display: block; width: 100%; overflow: hidden; height: 0px;"></div></td></tr></tbody></table></td></tr></tbody></table></div><div class="cube hasContent"><table cellpadding="0" cellspacing="0" width="100%" align="center" aria-hidden="true" class="widget_1_0_4" style="width: 100% !important; padding: 10px; box-sizing: border-box; background-color: rgb(199, 199, 199); line-height: normal; font-size: 14px;"><tbody><tr><td class="Widget index-module_Widget_3Alx7" style="width: 100% !important;"><table cellpadding="0" cellspacing="0" border="0" width="100%" class="tinymce-wrap index-module_WidgetText_2MGea" style="font-size: 14px;"><tbody><tr><td><div><p style="margin: 0;padding: 0;text-align: center;"><span style="font-family: impact, chicago; font-size: 36px;"><strong><span style="color: #040f5b;">XXXXX</span></strong></span></p></div><div style="clear: both; display: block; width: 100%; overflow: hidden; height: 0px;"></div></td></tr></tbody></table></td></tr></tbody></table></div><div class="cube hasContent"><table cellpadding="0" cellspacing="0" width="100%" align="center" aria-hidden="true" class="widget_1_0_5" style="width: 100% !important; padding: 10px; box-sizing: border-box; line-height: normal; font-size: 14px;"><tbody><tr><td class="Widget index-module_Widget_3Alx7" style="width: 100% !important;"><table aria-hidden="true" cellpadding="0" cellspacing="0" border="0" align="center" width="100%" class="WidgetBlank"><tbody><tr><td align="center" height="10"><table aria-hidden="true" cellpadding="0" cellspacing="0" border="0" align="center" width="100%"><tbody><tr><td></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></div></th></tr></tbody></table></div></td></tr><tr><td align="center"><div class="cube hasContent"><table bgcolor="#26004D" aria-hidden="true" border="0" cellpadding="0" cellspacing="0" width="100%" class="py-shapeWrap" style="max-width: 600px; margin: 0px auto; width: 100%; background-color: rgb(38, 0, 77); background-image: url(&quot;undefined&quot;); background-position: center center; background-size: cover;"><tbody><tr><th valign="top" class="py-colWrap" style="width: 100%; font-weight: normal; padding: 0px; text-align: initial;"><div class="cube hasContent"><table cellpadding="0" cellspacing="0" width="100%" align="center" aria-hidden="true" class="widget_2_0_0" style="width: 100% !important; padding: 10px; box-sizing: border-box; background-color: rgb(232, 232, 232); line-height: normal; font-size: 14px;"><tbody><tr><td class="Widget index-module_Widget_3Alx7" style="width: 100% !important;"><table aria-hidden="true" cellpadding="0" cellspacing="0" border="0" align="center" width="100%" class="WidgetBlank"><tbody><tr><td align="center" height="20"><table aria-hidden="true" cellpadding="0" cellspacing="0" border="0" align="center" width="100%"><tbody><tr><td></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></div><div class="cube hasContent"><table cellpadding="0" cellspacing="0" width="100%" align="center" aria-hidden="true" class="widget_2_0_1" style="width: 100% !important; padding: 10px; box-sizing: border-box; background-color: rgb(232, 232, 232); line-height: normal; font-size: 14px;"><tbody><tr><td class="Widget index-module_Widget_3Alx7" style="width: 100% !important;"><table cellpadding="0" cellspacing="0" border="0" width="100%" class="tinymce-wrap index-module_WidgetText_2MGea" style="font-size: 14px;"><tbody><tr><td><div><p style="margin: 0;padding: 0;text-align: center;"><span style="color: #000000;">灵感之城中枢局</span></p></div><div style="clear: both; display: block; width: 100%; overflow: hidden; height: 0px;"></div></td></tr></tbody></table></td></tr></tbody></table></div></th></tr></tbody></table></div></td></tr></tbody></table><style type="text/css" id="myStyle">.py-templateWrap, .py-templateWrap tr td, .py-templateWrap tr th{font-size: 14px; font-family: 微软雅黑;}.py-templateWrap a{color: ;}@media screen and (max-width: 768px){.py-shapeWrap-mobileFit .py-colWrap{width: '100% !important'; display: 'block !important';}}</style></body></html>"""

def email_send(verify_code,receiver):
    sender = 'x_MUSE@qq.com'  # 发件人邮箱
    password = 'hdkcncganyyqefab'  # 发件人邮箱授权码
    print(receiver)
    html = html_c.replace("XXXXX",verify_code)
    # msg = MIMEText(f'绑定QQ，验证码{verify_code}', 'plain', 'utf-8')
    msg = MIMEText(html, 'plain', 'utf-8')
    msg['From'] = formataddr(('MUSE', sender))
    msg['To'] = formataddr(('灵感者', receiver))
    msg['Subject'] = '灵感之城中枢系统账号绑定'

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # QQ邮箱的SMTP服务器及端口号
        server.login(sender, password)  # 登录QQ邮箱
        server.sendmail(sender, [receiver], msg.as_string())  # 发送邮件
        server.quit()  # 退出SMTP服务器
        print("邮件发送成功！")
        return 1
    except Exception as err:
        print("邮件发送失败！错误信息：", err)
        return 0

def qq_bind(message:Message):
    msg = message.content
    qq_email_pattern = r'[1-9]\d{7,10}'
    qq = re.findall(qq_email_pattern, msg)
    qq_email = f"{qq[0]}@qq.com"

    bind_state = r.get(f"personal_information_code:{message.author.id}")
    if bind_state != None:
        return message.reply(content = f"验证码已发送，请前往邮箱查看验证码")
    
    is_bind = r.hget(f"personal_information:{message.author.id}:information","qq")  #判断是否已绑定
    if is_bind == None:
        pass
    else:
        return message.reply(content = "你已绑定过QQ，无需重复绑定")
    
    for key in r.scan_iter('personal_information:*'):
        # 查询该QQ是否存在于当前的 hash 表中
        print(r.hget(key, "qq"))
        if qq[0] == r.hget(key, "qq"):
            return message.reply(content = f"当前QQ已被绑定")

    #判断QQ是否合法
    if qq == None:
        return message.reply(content="QQ不合法，请检查后重新绑定")
    
    #生成5位验证码
    verify_code = ''.join(str(random.randint(0, 9)) for i in range(5))
    verify_state = f"{verify_code}:{qq[0]}"
    r.setex(f"personal_information_code:{message.author.id}",300,verify_state)

    if email_send(verify_code,qq_email) == 0:
        return message.reply(content = "发送邮件失败，请重试")

    return message.reply(content = f"""验证码已发送到邮箱：
{qq[0]}@qq·com
请及时查看并在五分钟内填写验证码
发送：“验证码xxxxxx”即可验证成功""")


def verify(message:Message,i):
    msg = message.content
    verify_code = msg.replace("验证码","")
    
    verify_code = verify_code[0:5]

    is_code = r.get(f"personal_information_code:{message.author.id}")
    if is_code == None:
        if i == 1:
            return 0
        return message.reply(content = "请先获取验证码")
    
    is_bind = r.hget(f"personal_information:{message.author.id}:information","qq")  #判断是否已绑定
    if is_bind == None:
        pass
    else:
        if i == 1:
            return 0
        return message.reply(content = "你已绑定过QQ，无需重复绑定")

    if int(verify_code) == int(is_code[0:5]):
        if i == 1:
            return 1
        qq = is_code.replace(f"{verify_code}:","")
        r.hset(f"personal_information:{message.author.id}:information","qq",qq)
        r.zincrby("scoreboard:积分",200,f"{message.author.id}")
        return message.reply(content = "绑定成功，已为您认证身份，200积分已入账")
    else:
        if i == 1:
            return 0
        return message.reply(content = "验证码错误")

def unbind(message:Message,i):
    is_bind = r.hget(f"personal_information:{message.author.id}:information","qq")  #判断是否已绑定
    if is_bind == None:
        if i == 1:
            return 0
        return message.reply("你还未绑定QQ，无法解绑")
    else:
        if i == 1:
            return 1
        r.hdel(f"personal_information:{message.author.id}:information","qq",is_bind)
        r.zincrby("scoreboard:积分",-200,f"{message.author.id}")
        return message.reply(content = "解绑成功")