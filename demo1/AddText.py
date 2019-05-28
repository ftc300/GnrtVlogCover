import time
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


strs = "GAME OF THRONES \n 权力的游戏"
imageFile = "../resize-raw/pic001_resize.png"
file_save_dir = "../raw/"
x = 20
y = 20
word_size = 50
word_css = "Paris.ttf"
font = ImageFont.truetype(word_css, word_size)
im1 = Image.open(imageFile)  # 打开图片
draw = ImageDraw.Draw(im1)
print(font.getsize(strs))
draw.text((x, y), strs, (255, 255, 0), font=font)  # 设置位置坐标 文字 颜色 字体
# prefix = str(int(time.time()))
im1.show()
im1.save("../text-raw/pic001_text.png", format="png")
del draw
im1.close()