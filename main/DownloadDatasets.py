from urllib.request import urlopen
from shutil import copyfileobj

celebA_url = "https://web.pslib.cz/getFile/id:17651/%C5%A0ablona%20MP-RP%202017.dotx"

def celebA():
    with urlopen(celebA_url) as response, open("../datasets/celebA", "wb") as output:
        copyfileobj(response, output)
        # print(response.getcode()) TODO: validace že tam ten soubor je


celebA()
