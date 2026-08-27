
from random import randint
from re import U
import requests
import json
import webbrowser
import urllib.request
import time

from PIL import Image
amount = 1
while amount < 10:
    amount = amount + 1
    rnum = randint(1,5)
    if rnum == 1:
        url = 'https://api.thecatapi.com/v1/images/search'
    else:
        if rnum == 3:
            url = 'https://some-random-api.ml/animal/birb'
        else:
            if rnum == 4:
                url = 'https://some-random-api.ml/animal/fox'  
            else:
                if rnum == 5:
                   url = 'https://some-random-api.ml/animal/kangaroo' 
                else:
                     url = 'https://api.thedogapi.com/v1/images/search'
                
    a = requests.get(url)
    ab = a.text
    abc = json.loads(ab)
    if rnum >= 3:
        print(abc["image"])
        url2 = abc["image"]
        webbrowser.open_new(url2)
    else:
        print(abc[0]["url"])
        url2 = abc[0]["url"]
        webbrowser.open_new(url2)
    time.sleep(2)
    # urllib.request.urlretrieve(
   # url2, "gfg.png")
  
#img = Image.open("gfg.png")
#img.show()