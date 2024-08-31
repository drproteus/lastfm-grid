import os
import tempfile
from lib import get_cover_art_grid
from flask import Flask, render_template, make_response, send_file, abort


app = Flask(__name__)


API_KEY = os.getenv("API_KEY")
IMG_WIDTH = 174


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/covers/<width>/<height>/<user>/<period>", methods=["POST"])
def get_covers(user, period, width, height):
    im = get_cover_art_grid(user, period, int(width), int(height), IMG_WIDTH, API_KEY)
    if im is None:
        abort(404)
    with tempfile.NamedTemporaryFile() as f:
        im.save(f.name, format="JPEG")
        return send_file(f.name, download_name="covers.jpg")





