# http://hankerzheng.com/blog/chenge-the-size-of-pic-by-python-pil
import os, re
from PIL import Image

_RAW_DIR = "../raw/"
_RE_INDEX = re.compile(u"pic(\d{3})\..+")

def parse_start():
    """
    parse the starter index in `./raw` dir
    """
    starter = os.listdir(_RAW_DIR)[0]
    res = _RE_INDEX.match(starter)
    if not res:
        raise ValueError("No Files Found!")
    else:
        return int(res.group(1))

def resizePic(img):
    """
    The photo in the gallery would only display the top 174px at max
    The photo is in 16:10 size
    The crop para is (left, upper, right, lower)
    """
    # make sure the cut in the near middle of the img
    if img.width/16 > img.height/10:
        # the image is too wide
        cut_width = img.height/10*16
        padding = (img.width - cut_width)/2
        cut = img.crop((padding,0 ,img.width-padding,img.height))
    else:
        # the image is too high
        cut_height = img.width/16*10
        padding_top = (img.height - cut_height)*0.3
        padding_bot = (img.height - cut_height)*0.7
        cut = img.crop((0, padding_top, img.width, img.height-padding_bot))
    resized = cut.resize((1280,800), resample=Image.LANCZOS)
    return resized

def runResize():
    starter = parse_start()
    file_cound = len(os.listdir(_RAW_DIR))
    for index in range(starter, starter + file_cound):
        this_name = _RAW_DIR+'/pic%03d.png' %index
        with Image.open(this_name) as img:
            _small = resizePic(img)
            _small.save("../resize-raw/pic%03d_resize.png"%index, format="png")

if __name__ == "__main__":
    runResize()