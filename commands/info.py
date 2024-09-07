import click
import requests
import tempfile
from ascii_magic import AsciiArt
from pylast import SIZE_LARGE
from PIL import Image


@click.command("fmfetch")
@click.pass_obj
@click.argument("username", type=click.STRING)
def fmfetch(network, username):
    user = network.get_user(username)
    with tempfile.NamedTemporaryFile() as temp:
        resp = requests.get(user.get_image(SIZE_LARGE))
        temp.write(resp.content)
        im = Image.open(temp.name, formats=["JPEG", "PNG", "GIF"])
    art = AsciiArt.from_pillow_image(im)
    art.to_terminal(columns=64)
