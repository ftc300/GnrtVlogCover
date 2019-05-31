import requests
from PIL import Image, ImageFont, ImageFilter, ImageDraw, ImageOps
import os
import time
import yaml

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
    img = resizePic(Image.open(outPath))
    img.save(outPath)
    return img


def mergeImages(img1, img2, x, y):
    target = Image.new('RGBA', img1.size, (0, 0, 0, 0))
    box = (0, 0, 1280, 800)  # 区域
    img2 = img2.convert("RGBA")
    img2 = img2.resize((1280,800))
    img1 = img1.convert("RGBA")
    img1 = img1.resize((1280,800))
    target.paste(img2, box)
    target.paste(img1, (x, y), img1)
    return target

# https://stackoverflow.com/questions/5324647/how-to-merge-a-transparent-png-image-with-another-image-using-pil
def mergeTransparentImageDirectly(bg,foreImg,x,y):
    bg.paste(foreImg, (x, y), mask=foreImg)
    return bg

def saveTextImg( x, y, r, content, font,font_size,textcolor, shadowcolor,angle):
    font = ImageFont.truetype(font, font_size)
    img_1 = Image.new("RGBA", (1280, 800), (0, 0, 0, 0))
    w, h = ImageDraw.Draw(img_1).textsize(content, font)
    iw = w + 3 * r
    ih = h + 3 * r
    img_2 = Image.new("RGBA", (1280, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_2)
    addTextBorder(draw, x, y, r, content, font, textcolor,shadowcolor)
    img_2 = img_2.rotate(angle, expand=True, center=((640, 800)))
    img_1.paste(img_2)
    # img_1.save("img/txt/"+str(int(time.time()))+".png")
    return img_1


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


def blurBackground(img, r=5):
    return img.filter(ImageFilter.GaussianBlur(radius=r))

def run():
    f = open('config.yaml', 'r', encoding='UTF-8')
    f = yaml.load(f)
    inBackgroundImg = f["inBackgroundImg"]
    inBackgroundImgResize = inBackgroundImg.split(".")[0]+ "resize.png"
    imgBg = Image.open(inBackgroundImg)
    inFocusImg = f["inFocusImg"]
    inFocusRmImg = inFocusImg.split(".")[0]+ "rmbg.png"
    imgFocus = Image.open(inFocusImg)

    # step one:resize background
    if notExist(inBackgroundImgResize):
        print("resize background")
        imgBg = resizePic(imgBg)
        imgBg.save(inputBackgroundImgResize)
    else:
        print("exist resize background , load...")
        imgBg = Image.open(inBackgroundImgResize)
    # step two
    imgBg = blurBackground(imgBg,f["blurR"])

    # step three: remove focus backgraound
    if notExist(inFocusRmImg):
        print("call remove bg api,then load ...")
        imgFocus = removeBg(inFocusImg, inFocusRmImg, f["apiKey"])
    else:
        print("exist remove bg , load ...")
        imgFocus = Image.open(inFocusRmImg)

    imgOutput = mergeImages(imgFocus,imgBg,400,0)

    # step four: add text
    for item in f["text"]:
        font = item["font"]
        font_size = item["font_size"]
        content = item["content"]
        r = item["r"]
        angle = item["angle"]
        x = item["x"]
        y = item["y"]
        textcolor = item["textcolor"]
        shadowcolor = item["shadowcolor"]
        imgTxt = saveTextImg( x, y, r, content, font,font_size,textcolor, shadowcolor,angle)
        imgOutput = mergeImages(imgTxt,imgOutput , 0, 0)

    for i in f["decoration"]:
        imgPath = i["img"]
        x = i["x"]
        y = i["y"]
        img = Image.open(imgPath)
        mergeTransparentImageDirectly(imgOutput,img,x,y)
    imgOutput.show()
    imgOutput.save(f["outputFile"] + str(int(time.time())) + ".png")



def notExist(path):
    return bool(1-os.path.exists(path))

if __name__ == "__main__":
    run()




