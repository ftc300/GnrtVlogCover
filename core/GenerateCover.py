import requests
from PIL import Image, ImageFont, ImageFilter, ImageDraw, ImageOps
import CoverText

def resizePic(img):
    # make sure the cut in the near middle of the img
    if img.width / 16 > img.height / 10:
        # the image is too wide
        cut_width = img.height / 10 * 16
        padding = (img.width - cut_width) / 2
        cut = img.crop((padding, 0, img.width - padding, img.height))
    else:
        # the image is too high
        cut_height = img.width / 16 * 10
        padding_top = (img.height - cut_height) * 0.3
        padding_bot = (img.height - cut_height) * 0.7
        cut = img.crop((0, padding_top, img.width, img.height - padding_bot))
    resized = cut.resize((1280, 800), resample=Image.LANCZOS)
    return resized


def removeBg(filePath, outPath, apiKey):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(filePath, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': apiKey},
    )
    if response.status_code == requests.codes.ok:
        with open(outPath, 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)
    return Image.open(outPath)


def addText(img, x, y, text, font_path="font/Paris.ttf", text_size=50, textColor="green", shaderColor="yellow"):
    font = ImageFont.truetype(font_path, text_size)
    d0 = ImageDraw.Draw(img)
    d0.textsize(text, font)
    txtImg = Image.new('L', d0.textsize(text, font))
    draw = ImageDraw.Draw(txtImg)
    draw.text((x - 2, y), text, font=font, fill=shaderColor)
    draw.text((x + 2, y), text, font=font, fill=shaderColor)
    draw.text((x, y - 2), text, font=font, fill=shaderColor)
    draw.text((x, y + 2), text, font=font, fill=shaderColor)
    # thicker border
    draw.text((x - 2, y - 2), text, font=font, fill=shaderColor)
    draw.text((x + 2, y - 2), text, font=font, fill=shaderColor)
    draw.text((x - 2, y + 2), text, font=font, fill=shaderColor)
    draw.text((x + 2, y + 2), text, font=font, fill=shaderColor)
    # now draw the text over it
    draw.text((x, y), text, font=font, fill=textColor)
    w = txtImg.rotate(0, expand=1)
    pass


def blurBackground(img, r=5):
    return img.filter(ImageFilter.GaussianBlur(radius=r))


def mergeImages(img1, img2 , x,y):
    target = Image.new('RGBA', img1.size, (0, 0, 0, 0))
    box = (0, 0, 1280, 800)  # 区域
    img2 = img2.convert("RGBA")
    img2 = img2.resize((box[2] - box[0], box[3] - box[1]))
    target.paste(img2, box)
    target.paste(img1, (x,y), img1)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域，将底图显示出来。
    target.rotate(30)
    target.show()






if __name__ == "__main__":
    pass
