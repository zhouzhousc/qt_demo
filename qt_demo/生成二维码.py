#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/5/15


import qrcode
from PIL import Image, ImageFile, ImageDraw

ImageFile.LOAD_TRUNCATED_IMAGES = True


# 设置中心图片四周圆角
def circle_crop_image(im):
    rad = 10  # 设置半径
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


# 生成二位码
def create_qr_code(url, file_name, icon_file=None):
    qr = qrcode.QRCode(
        version=5,
        # 设置容错率为最高
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=6,
        border=4,
    )
    qr.add_data(url)
    # 添加二维码内容，可以直接是字符串文本，也可url链接

    qr.make(fit=True)

    img = qr.make_image(fill_color="#3ac25b", back_color="#FFF")
    # 设置二维码为彩色
    img = img.convert("RGBA")
    if icon_file:
        icon = Image.open(icon_file)
        w, h = img.size
        factor = 4
        size_w = int(w / factor)
        size_h = int(h / factor)
        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
        w = int((w - icon_w) / 2)
        h = int((h - icon_h) / 2)
        icon = icon.convert("RGBA")

        # ------以下是进一步处理中心图片，可省略------
        # 白底图
        white_img = Image.new("RGBA", (icon_w + 6, icon_h + 6), (255, 255, 255))
        # 白底图圆角处理
        # white_img = circle_crop_image(white_img)
        # 灰底图
        gray_img = Image.new("RGBA", (icon_w + 2, icon_h + 2), (230, 230, 230))
        # 灰底图圆角处理
        gray_img = circle_crop_image(gray_img)
        # 粘贴灰底图
        white_img.paste(gray_img, (2, 2))
        # 粘贴白图
        img.paste(white_img, (w - 2, h - 2))
        # icon处理圆角
        icon = circle_crop_image(icon)
        # ----------------以上----------------

        # 粘贴icon
        img.paste(icon, (w + 1, h + 1))
    img.show()
    img.save('' + file_name + '.png', quality=100)


icon_path = "logo.jpg"  # 中心图片
create_qr_code('http://www.baidu.com', "hnww", "logo.jpg")
