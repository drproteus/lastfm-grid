import os
import requests
import json
import threading
import tempfile
from collections import OrderedDict
from PIL import Image


API_KEY = os.getenv("API_KEY")
user = "Zarhyn"
period = "3month"
size = 5
img_width = 174
outfile = "/Users/jake/covers.jpg"


url = "https://ws.audioscrobbler.com/2.0"


resp = requests.get(url, params={
    "method": "user.gettopalbums",
    "user": user,
    "period": period,
    "api_key": API_KEY,
    "format": "json",
})

topalbums = json.loads(resp.content)["topalbums"]["album"]

covers = OrderedDict()
for album in topalbums:
    images = album["image"]
    image_url = None
    for image in images:
        if image["size"] == "large":
            image_url = image["#text"]
    if image_url:
        covers[image_url] = None
        print(album["name"])
        if len(covers) >= size ** 2:
            break


def load_resize_cover(cover_url):
    resp = requests.get(cover_url)
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(resp.content)
        covers[cover_url] = Image.open(temp.name)
        covers[cover_url].resize((img_width, img_width))


thds = []
for cover_url in covers:
    thd = threading.Thread(target=load_resize_cover, args=(cover_url,))
    thds.append(thd)
    thd.start()

for thd in thds:
    thd.join()

im = Image.new(mode="RGB", size=(img_width * size, img_width * size))
for i, (cover_url, cover_image) in enumerate(covers.items()):
    box = (img_width * i, img_width * i)
    w = img_width * (i % size)
    h = img_width * (i // size)
    im.paste(cover_image, box=(w, h))

im.save(outfile)


