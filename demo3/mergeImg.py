# https://blog.csdn.net/guduruyu/article/details/71439733
# https://www.cnblogs.com/lilinwei340/p/6474170.html
# https://stackoverflow.com/questions/37941648/unable-to-crop-away-transparency-neither-pil-getbbox-nor-numpy-are-working
from PIL import Image
from PIL import ImageChops
import numpy as np
import matplotlib.pyplot as plt
path1 = "../gaus-raw/pic004_gaus.png"
path2 = "../resize-raw/pic005_resize.png"
outPath = "../merge-raw/merge.png"


def mergeByPaste():
    img = Image.open(path2, 'r')
    img = img.convert('RGBA')
    img_w, img_h = img.size
    # background = Image.new('RGBA', (1280, 800), (255, 255, 255, 255))
    background = Image.open(path1)
    background = background.convert("RGBA")
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, offset)
    background.save(outPath)
    background.show()

# select this  type
def mergeByPaste2():
    base_img = Image.open(path2)
    # Image.new(mode, size, color=0)，color可以用tuple表示，分别表示RGBA的值
    target = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    box = (0, 0, 1280, 800)  # 区域
    region = Image.open(path1)
    region = region.convert("RGBA")
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    target.paste(region, box)
    cropImg = cutTransparentRegion(base_img)
    offsetImg = setPosition(target,cropImg,1,1)
    target.paste(base_img, offsetImg, base_img)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域，将底图显示出来。
    target.rotate(30)
    target.show()
    target.save(outPath)  # 保存图片


def mergeByComposite():
    img1 = Image.open(path1)
    img1 = img1.convert('RGBA')
    img2 = Image.open(path2)
    img2 = img2.convert('RGBA')
    r, g, b, alpha = img2.split()
    alpha = alpha.point(lambda i: i > 0 and 204)
    img = Image.composite(img2, img1, alpha)
    img.save(outPath)
    img.show()


def mergeByBlend():
    img1 = Image.open(path1)
    img1 = img1.convert('RGBA')
    img2 = Image.open(path2)
    img2 = img2.convert('RGBA')
    img = Image.blend(img1, img2, 0.5)
    img.save(outPath)
    img.show()


def cutTransparentRegion(image):
    image.load()
    image_data = np.asarray(image)
    image_data_bw = image_data[:, :, 3]
    non_empty_columns = np.where(image_data_bw.max(axis=0) > 0)[0]
    non_empty_rows = np.where(image_data_bw.max(axis=1) > 0)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows),
               min(non_empty_columns), max(non_empty_columns))
    image_data_new = image_data[cropBox[0]:cropBox[
        1] + 1, cropBox[2]:cropBox[3] + 1, :]
    new_image = Image.fromarray(image_data_new)
    return new_image


def autocrop_image(image, border=0):
    bbox = image.getbbox()
    image = image.crop(bbox)
    (width, height) = image.size
    width += border * 2
    height += border * 2
    cropped_image = Image.new("RGBa", (width, height), (0, 0, 0, 0))
    cropped_image.paste(image, (border, border))
    return cropped_image


def setPosition(imgBg,imgFore,xRatio = 0.5,yRation = 0.5):
    foreW,foreH = imgFore.size
    bgW,bgH = imgBg.size
    offset = (int((bgW - foreW)*xRatio), int((bgH - foreH)*yRation))
    return offset



mergeByPaste2()
