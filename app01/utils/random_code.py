# 引入PIL库 pip install pillow

from PIL import Image, ImageDraw, ImageFont
import string
import random
from io import BytesIO


# 随机颜色
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


str_all = string.digits + string.ascii_letters


def random_code(size=(200, 42), length=4, point_num=100, line_num=15):
    weight, height = size
    img = Image.new('RGB', size, color=(255, 255, 255))

    draw = ImageDraw.Draw(img)  # 生成一个画布

    font = ImageFont.truetype(font='static/my/font/balade-9yjo2.otf', size=20)

    # 书写文字
    valid_code = ''
    for i in range(length):
        random_char = random.choice(str_all)
        draw.text((30 + 40 * i, -2), random_char, (0, 0, 0), font=font)
        valid_code += random_char
    print(valid_code)



    # 对图像处理一下
    # 画点
    for i in range(point_num):
        x = random.randint(0, weight)
        y = random.randint(0, height)
        draw.point((x, y), random_color())

    # 画线
    for i in range(line_num):
        x1 = random.randint(0, weight)
        y1 = random.randint(0, height)
        x2 = random.randint(0, weight)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), random_color())

    # 创建一个内存句柄
    f = BytesIO()
    # 将图片保存到内存句柄中
    img.save(f, 'PNG')
    # 读取内存句柄即可
    data = f.getvalue()
    return (data, valid_code)

if __name__ == "__main__":
    random_code()