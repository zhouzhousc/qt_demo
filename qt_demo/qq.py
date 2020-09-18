#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/5/13


'''
==============================
test1：生成二维码及查看
==============================
'''
from PIL import Image
import qrcode

qr = qrcode.QRCode(
    version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=6, border=6)
qr.add_data("这里是二维码信息！")
qr.make(fit=True)
# 问题就出在这个地方，如果要生成白底黑码的二维码必须要在这里以RGB的方式指定颜色。
img = qr.make_image(fill_color="#3ac25b", back_color="#FFF")
img = img.convert("RGBA")

icon = Image.open("logo.jpg")  # 这里是二维码中心的图片

img_w, img_h = img.size
factor = 4
size_w = int(img_w / factor)
size_h = int(img_h / factor)

icon_w, icon_h = icon.size
if icon_w > size_w:
    icon_w = size_w
if icon_h > size_h:
    icon_h = size_h
icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

w = int((img_w - icon_w) / 2)
h = int((img_h - icon_h) / 2)
icon = icon.convert("RGBA")
img.paste(icon, (w, h), icon)
img.show()   # 显示图片,可以通过save保存
img.save("logo.png")

