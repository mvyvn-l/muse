# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageOps
import matplotlib.backends.backend_agg as agg

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
matplotlib.rcParams['font.sans-serif'] = ['SimHei']


import numpy as np

from io import BytesIO

def chart(sm,zl,wl,mj,fy,name):
    # 数据
    labels = np.array(['生命', '智力', '武力', '敏捷', '防御'])
    data = np.array([sm, zl, wl, mj, fy])

    max_value = max(sm, zl, wl, mj, fy)
    min_value = min(sm, zl, wl, mj, fy)
    min_value = str(int(min_value) - 50)
    print("max:",max_value,"   min:",min_value)

    # 画图
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    data = np.concatenate((data, [data[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig = plt.figure(figsize=(6,6))

    ax = fig.add_subplot(111, polar=True)
    #ax.set_ylim(min_value,max_value)
    #ax.set_rmax(max_value)#设置极坐标轴的上限
    #ax.set_rman(min_value)#设置极坐标轴的下限
    ax.plot(angles, data, 'ko-', linewidth=2,alpha=0.8)
    ax.fill(angles, data, facecolor='gray', alpha=0.2)
    ax.set_thetagrids(angles[:-1] * 180/np.pi, labels, fontsize=20)
    ax.tick_params(labelsize=20)
    ax.set_rlabel_position(20)
    #ax.set_title(f"{name}的属性分析图", va='bottom',fontsize=20)
    ax.grid(True)

    #img2=Image.open("E:\Desktop桌面\muse\\test\\testj.jpg")
    img = Image.new('RGB', (600, 600), (255, 255, 255))
    # 将Matplotlib图像转换为Pillow图像
    fig.canvas = agg.FigureCanvasAgg(fig)
    fig.canvas.draw()
    buf = fig.canvas.buffer_rgba()
    matplotlib_image = np.asarray(buf)
    pillow_image = Image.fromarray(matplotlib_image)

    pillow_image =pillow_image.resize((600, 600))

    #plt.show()
    # 合并pillow_image到img2上面
    img.paste(pillow_image, (0, 0))

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("E:\Desktop桌面\Design_Work\字体\楷体.ttf", 50)
    draw.text((20, 530), f"{name}", (0, 0, 0), font=font)

    # 将文件保存为二进制文件流
    img1_bytes = BytesIO()  # 创建一个二进制对象 并将图像内容写入到二进制对象中 获得一个二进制图像文件类型
    img.save(img1_bytes, format="PNG")

    return img1_bytes
    
