# https://blog.csdn.net/guduruyu/article/details/71439733
# https://www.cnblogs.com/lilinwei340/p/6474170.html
# https://stackoverflow.com/questions/37941648/unable-to-crop-away-transparency-neither-pil-getbbox-nor-numpy-are-working
from PIL import Image
from PIL import ImageChops
import numpy as np
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


def mergeByPaste2():
    # 加载中间透明的手机图片
    base_img = Image.open(path2)
    # 新建透明底图，大小和手机图一样，mode使用RGBA，保留Alpha透明度，颜色为透明
    # Image.new(mode, size, color=0)，color可以用tuple表示，分别表示RGBA的值
    target = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    box = (0, 0, 1280, 800)  # 区域
    # 加载需要狐狸像
    region = Image.open(path1)
    # region = region.rotate(180)  # 旋转180度
    # 确保图片是RGBA格式，大小和box区域一样
    region = region.convert("RGBA")
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    # 先将狐狸像合成到底图上
    target.paste(region, box)
    # 将手机图覆盖上去，中间透明区域将狐狸像显示出来。
    target.paste(base_img, (0, 0), base_img)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域，将底图显示出来。

    target.show()
    target.save(outPath)  # 保存图片


def mergeByComposite():
    img1 = Image.open(path1)
    img1 = img1.convert('RGBA')
    img2 = Image.open(path2)
    img2 = img2.convert('RGBA')
    img2 = ImageChops.offset(img2, 200, 0)
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

def autocrop_image2(image):
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

# mergeByPaste()
# mergeByPaste2()
mergeByComposite()
# mergeByBlend()
# im = Image.open("../raw/pic005.png")
# (387, 293)
# im = Image.open(path2)
# (789, 598)
# cropped = autocrop_image2(im)
# print(cropped.size)
# cropped.show()