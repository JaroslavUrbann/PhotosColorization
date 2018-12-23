from urllib.request import urlopen
from shutil import copyfileobj

celebA_url = "https://www.dropbox.com/sh/8oqt9vytwxb3s4r/AADIKlz8PR9zr6Y20qbkunrba/Img/img_align_celeba.zip?dl=1&pv=1"


def celebA():
    with urlopen(celebA_url) as response, open("../datasets/celebA", "wb") as output:
        copyfileobj(response, output)
        # print(response.getcode()) TODO: validace že tam ten soubor je


celebA()
