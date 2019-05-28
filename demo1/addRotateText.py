from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps

imageFile = "../resize-raw/pic001_resize.png"
im = Image.open(imageFile)

word_size = 50
word_css = "Paris.ttf"
text = u"权力的游戏 \n  Game Of Thrones"
font = ImageFont.truetype(word_css, word_size)
d0 = ImageDraw.Draw(im)
d0.textsize(text, font)
txt = Image.new('L', d0.textsize(text, font))
d = ImageDraw.Draw(txt)
d.text((0, 0), text, font=font, fill=255)
w = txt.rotate(0, expand=1)
im.paste(ImageOps.colorize(w, (0, 0, 0), (255, 255, 84)), (242, 60), w)
im.save("rotate.png")
