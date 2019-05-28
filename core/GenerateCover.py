import requests
from PIL import Image, ImageFont, ImageFilter, ImageDraw, ImageOps


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

def addText():
    pass


def blurBackground(img, r=5):
    return img.filter(ImageFilter.GaussianBlur(radius=r))


if __name__ == "__main__":
    pass
