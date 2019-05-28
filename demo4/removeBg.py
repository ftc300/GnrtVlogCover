import requests
from PIL import ImageDraw

def removeBg(filePath,outPath,apiKey):
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

if __name__ == "__main__":
    _filePath_ = "../raw/pic003.png"
    _outPath_ = "../removebg-raw/pic003_no_bg.png"
    _apiKey_ = "uLUKsbfqwbfWvZekocsq4jUf"
    removeBg(_filePath_,_outPath_,_apiKey_)