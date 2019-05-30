from PIL import Image, ImageDraw, ImageFont
import os


def mergeImages(img1, img2, x, y):
    target = Image.new('RGBA', img1.size, (0, 0, 0, 0))
    box = (0, 0, 1280, 800)  # 区域
    img2 = img2.convert("RGBA")
    img2 = img2.resize((1280,800))
    target.paste(img2, box)
    target.paste(img1, (x, y), img1)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域，将底图显示出来。
    target.rotate(30)
    target.show()


def saveTextImg( x, y, r, content, font,textcolor, shadowcolor,angle,outPath):
    font = ImageFont.truetype(font, font_size)
    img_1 = Image.new("RGBA", (1280, 800), (0, 0, 0, 0))
    w, h = ImageDraw.Draw(img_1).textsize(content, font)
    iw = w + 3 * r
    ih = h + 3 * r
    img_2 = Image.new("RGBA", (1280, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_2)
    addTextBorder(draw, x, y, r, content, font, textcolor,shadowcolor)
    img_2 = img_2.rotate(angle, expand=True, center=((w + 2 * r) / 2, (h + 2 * r) / 2))
    img_1.paste(img_2)
    img_1.save(outPath)


def addTextBorder(draw, x, y, r, text, font, textcolor, shadowcolor):
    draw.text((x - r, y), text, font=font, fill=shadowcolor)
    draw.text((x + r, y), text, font=font, fill=shadowcolor)
    draw.text((x, y - r), text, font=font, fill=shadowcolor)
    draw.text((x, y + r), text, font=font, fill=shadowcolor)
    draw.text((x - r, y - r), text, font=font, fill=shadowcolor)
    draw.text((x + r, y - r), text, font=font, fill=shadowcolor)
    draw.text((x - r, y + r), text, font=font, fill=shadowcolor)
    draw.text((x + r, y + r), text, font=font, fill=shadowcolor)
    draw.text((x, y), text, fill=textcolor, font=font)