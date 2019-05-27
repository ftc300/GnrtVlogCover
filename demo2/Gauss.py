from PIL import Image, ImageFilter


def main():
    path = "../resize-raw/pic004_resize.png"
    im = Image.open(path)
    gbF = im.filter(ImageFilter.GaussianBlur(radius=5))
    gbF.save("../gaus-raw/pic004_gaus.png")
main()

