
from PIL import Image, ImageDraw, ImageFont
import os

def mergeImages(img1, img2 , x,y):
    target = Image.new('RGBA', img1.size, (0, 0, 0, 0))
    box = (0, 0, 1280, 800)  # 区域
    img2 = img2.convert("RGBA")
    img2 = img2.resize((box[2] - box[0], box[3] - box[1]))
    target.paste(img2, box)
    target.paste(img1, (x,y), img1)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域，将底图显示出来。
    target.rotate(30)
    target.show()

def  o():
    imageFile = "../resize-raw/pic001_resize.png"
    x = 10
    y = 10
    im = Image.open(imageFile)
    word_size = 50
    word_css = "Paris.ttf"
    text = u"权力的游戏 \n  Game Of Thrones"
    font = ImageFont.truetype(word_css, word_size)
    d0 = ImageDraw.Draw(im)
    d0.textsize(text, font)
    txt = Image.new('RGBA', d0.textsize(text, font))
    draw = ImageDraw.Draw(txt)
    draw.text((x - 2, y), text, font=font, fill=123)
    draw.text((x + 2, y), text, font=font, fill=123)
    draw.text((x, y - 2), text, font=font, fill=123)
    draw.text((x, y + 2), text, font=font, fill=123)

    # thicker border
    draw.text((x - 2, y - 2), text, font=font, fill=123)
    draw.text((x + 2, y - 2), text, font=font, fill=123)
    draw.text((x - 2, y + 2), text, font=font, fill=123)
    draw.text((x + 2, y + 2), text, font=font, fill=123)

    draw.text((x, y), text, font=font, fill=255)
    w = txt.rotate(0, expand=1)
    mergeImages(im,w,0,0)


path1 = "../gaus-raw/pic004_gaus.png"
path2 = "../resize-raw/pic005_resize.png"
img1 = Image.open(path1, 'r')
img1 = img1.convert('RGBA')
img2 = Image.open(path2, 'r')
img2 = img2.convert('RGBA')
mergeImages(img2,img1,100,100)