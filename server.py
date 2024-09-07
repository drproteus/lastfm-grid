import os
import tempfile
from lib.images import get_cover_art_grid
from flask import Flask, render_template, send_file, abort
from pylast import LastFMNetwork


API_KEY = os.getenv("API_KEY")
assert API_KEY is not None, "Environment variable API_KEY missing!"


app = Flask(__name__)
network = LastFMNetwork(api_key=API_KEY)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/covers/<width>/<height>/<username>/<period>", methods=["POST"])
def get_covers(username, period, width, height):
    im = get_cover_art_grid(network, username, period, int(width), int(height))
    if im is None:
        abort(404)
    with tempfile.NamedTemporaryFile() as f:
        im.save(f.name, format="JPEG")
        return send_file(f.name, download_name="covers.jpg")
