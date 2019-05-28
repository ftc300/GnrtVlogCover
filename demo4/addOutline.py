from PIL import Image

r = 2 ;
img = Image.open("../removebg-raw/pic003_no_bg.png").convert("L")
width,height = img.size
data = []
for i in range(r,width-r):
    for j in range(r,height-r):
        # getpixel =>(r, g, b, alpha)
        currentAlpha = img.getpixel((i,j))
        lastAlpha = img.getpixel((i,j-1))
        if (currentAlpha ==0 and lastAlpha!=0 ) or (lastAlpha ==0 and currentAlpha != 0):
            data.append((i,j))

img1 = Image.open("../removebg-raw/pic003_no_bg.png")
for item in data:
    img1.putpixel((item[0]-r,item[1]), (0, 0, 255, 255))
    img1.putpixel((item[0]+r,item[1]), (0, 0, 255, 255))
    img1.putpixel((item[0],item[1]+r), (0, 0, 255, 255))
    img1.putpixel((item[0],item[1]-r), (0, 0, 255, 255))

    img1.putpixel((item[0]-r,item[1]-r), (0, 0, 255, 255))
    img1.putpixel((item[0]+r,item[1]+r), (0, 0, 255, 255))
    img1.putpixel((item[0]-r,item[1]+r), (0, 0, 255, 255))
    img1.putpixel((item[0]+r,item[1]-r), (0, 0, 255, 255))
# img1 = img.convert("RGBA")
img1.save("../removebg-raw/pic004_no_bg_outline.png")
