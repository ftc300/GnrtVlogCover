# https://blog.csdn.net/guduruyu/article/details/71439733
from PIL import Image


def blend_two_images2():
    img1 = Image.open("bridge.png ")
    img1 = img1.convert('RGBA')

    img2 = Image.open("birds.png ")
    img2 = img2.convert('RGBA')

    r, g, b, alpha = img2.split()
    alpha = alpha.point(lambda i: i > 0 and 204)

    img = Image.composite(img2, img1, alpha)

    img.show()
    img.save("blend2.png")

