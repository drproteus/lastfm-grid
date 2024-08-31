import json
import requests
import tempfile
import threading
from PIL import Image
from collections import OrderedDict


def get_cover_art_grid(user, period, size, img_width, api_key):
    url = "https://ws.audioscrobbler.com/2.0"

    resp = requests.get(url, params={
        "method": "user.gettopalbums",
        "user": user,
        "period": period,
        "api_key": api_key,
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
    return im
