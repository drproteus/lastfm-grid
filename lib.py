import requests
import tempfile
import threading
from pylast import SIZE_LARGE
from PIL import Image
from collections import OrderedDict
from typing import Optional


IMG_WIDTH = 174


def get_cover_art_grid(
    network,
    username,
    period,
    width,
    height,
    img_width=IMG_WIDTH,
) -> Optional[Image.Image]:
    user = network.get_user(username)
    top_albums = user.get_top_albums(period=period, limit=width * height + 10)

    covers = OrderedDict()
    for album in top_albums:
        image_url = album.item.get_cover_image(SIZE_LARGE)
        if image_url:
            covers[image_url] = None
            if len(covers) >= width * height:
                break

    def load_resize_cover(cover_url):
        resp = requests.get(cover_url)
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(resp.content)
            temp.seek(0)
            try:
                covers[cover_url] = Image.open(temp.name, formats=["JPEG", "PNG", "GIF"])
                covers[cover_url].resize((img_width, img_width))
            except Exception as e:
                print(e)
                print(cover_url)

    thds = []
    for cover_url in covers:
        thd = threading.Thread(target=load_resize_cover, args=(cover_url,))
        thds.append(thd)
        thd.start()

    for thd in thds:
        thd.join()

    im = Image.new(mode="RGB", size=(img_width * width, img_width * height))
    for i, (cover_url, cover_image) in enumerate(covers.items()):
        w = img_width * (i % width)
        h = img_width * (i // width % height)
        try:
            im.paste(cover_image, box=(w, h))
        except Exception as e:
            print(e)
    return im
