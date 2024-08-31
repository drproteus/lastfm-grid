import os
import tempfile
from lib import get_cover_art_grid
from flask import Flask, render_template, make_response, send_file


app = Flask(__name__)


API_KEY = os.getenv("API_KEY")
IMG_WIDTH = 174


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/covers/<size>/<user>/<period>", methods=["POST"])
def get_covers(user, period, size):
    im = get_cover_art_grid(user, period, int(size), IMG_WIDTH, API_KEY)
    with tempfile.NamedTemporaryFile() as f:
        im.save(f.name, format="JPEG")
        return send_file(f.name, download_name="covers.jpg")





