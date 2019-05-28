from PIL import Image, ImageDraw, ImageFont
import os


# 用于文字边框展示，传入draw,坐标x,y，字体，边框颜色和填充颜色
def text_border(draw, x, y, font, shadowcolor, fillcolor):
    # thin border
    draw.text((x - 2, y), text, font=font, fill=shadowcolor)
    draw.text((x + 2, y), text, font=font, fill=shadowcolor)
    draw.text((x, y - 2), text, font=font, fill=shadowcolor)
    draw.text((x, y + 2), text, font=font, fill=shadowcolor)

    # thicker border
    draw.text((x - 2, y - 2), text, font=font, fill=shadowcolor)
    draw.text((x + 2, y - 2), text, font=font, fill=shadowcolor)
    draw.text((x - 2, y + 2), text, font=font, fill=shadowcolor)
    draw.text((x + 2, y + 2), text, font=font, fill=shadowcolor)

    # now draw the text over it
    draw.text((x, y), text, font=font, fill=fillcolor)


x, y = 1280/2, 800/2

fname2 = "../resize-raw/pic003_resize.png"
im = Image.open(fname2)
pointsize = 50
fillcolor = "green"
shadowcolor = "yellow"
text = "GAME OF THRONES \n 权力的游戏"
font = "Paris.ttf"
txt=Image.new('L', (500,50))
draw = ImageDraw.Draw(im)
font = ImageFont.truetype(font, pointsize)
# 调用函数
text_border(draw, x, y, font, shadowcolor, fillcolor)


fname2 = "../text-raw/pic003_text_border.png"
im.save(fname2)
im.show()