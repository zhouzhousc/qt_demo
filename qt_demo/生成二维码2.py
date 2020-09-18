# coding = utf-8
# 二维码生成

import qrcode
from PIL import Image, ImageDraw


# 设置圆角
def circle_crop_image(im, radii):
    # 创建一个黑色背景的画布
    circle = Image.new('L', (radii * 2, radii * 2), 0)
    # 画黑色方形
    draw = ImageDraw.Draw(circle)
    # 画白色圆形
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)
    # 把原图转换成RGBA模式，增加alpha通道
    img = im.convert("RGBA")
    w, h = img.size
    # 画4个角（将整圆分离为4个部分）再粘贴到alpha通道
    alpha = Image.new('L', img.size, 255)
    # 左上角
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))
    # 右上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))
    # 右下角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))
    # 左下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))
    # 白色区域透明可见，黑色区域不可见
    img.putalpha(alpha)
    return img


# 生成二位码
def create_qr_code(url, icon_file, file_name, save_path):
    qr = qrcode.QRCode(
        version=5,
        # 设置容错率为最高
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=6,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#3ac25b", back_color="#FFF")
    img = img.convert("RGBA")
    icon = Image.open(icon_file)
    # 把RGB的图转换成RGBA模式，处理alpha透明通道（后边替换透明为白色）
    icon = icon.convert("RGBA")
    w, h = img.size
    icon_w, icon_h = icon.size
    # 超过80的压缩到80
    if icon_w > 80:
        icon = icon.resize((80, 80), Image.ANTIALIAS)
        icon_w, icon_h = icon.size
        w = int((w - 80) / 2)
        h = int((h - 80) / 2)
    else:
        w = int((w - icon_w) / 2)
        h = int((h - icon_h) / 2)
    # 把png背景色转换为白色，避免处理裁剪圆角时出现黑边
    w_d = Image.new('RGBA', icon.size, (255, 255, 255))
    w_d.paste(icon, (0, 0, icon_w, icon_h), icon)
    # r = icon_w // 15
    r = 6
    icon = circle_crop_image(w_d, r)
    # 白底图（尺寸大小）
    white_img = Image.new("RGBA", (icon_w+20, icon_h+20), (255, 255, 255))
    white_img = circle_crop_image(white_img, r)
    # 灰底图
    gray_img = Image.new("RGBA", (icon_w, icon_h), (230, 230, 230))
    # 灰底图圆角处理
    gray_img = circle_crop_image(gray_img, r)
    # 粘贴灰底图（起点坐标 = （白图长 - 灰图长） / 2）
    white_img.paste(gray_img, (10, 10), gray_img)
    # 粘贴白图（位置起点坐标）
    img.paste(white_img, (w-5, h-5), white_img)
    # 粘贴icon（起点坐标）
    img.paste(icon, (w + 5, h + 5), icon)
    save_file = save_path + file_name + '.png'
    img.save(save_file, quality=100)
    # img.show()
    return save_file


if __name__ == '__main__':
    icon_path = 'logo.jpg'
    save_path = 'E:/qt_demo/'
    create_qr_code('http://www.zhousc.cn', icon_path, 'cs', save_path)
