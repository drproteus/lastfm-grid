import click
from pylast import (
    PERIOD_12MONTHS,
    PERIOD_1MONTH,
    PERIOD_3MONTHS,
    PERIOD_6MONTHS,
    PERIOD_OVERALL,
    PERIOD_7DAYS,
)
from lib.images import get_cover_art_grid
from ascii_magic import AsciiArt
from startfile import startfile


@click.command("album-grid")
@click.pass_obj
@click.argument("username", type=click.STRING)
@click.argument("output", type=click.File("wb"))
@click.option(
    "--period",
    "-p",
    type=click.Choice(
        [
            PERIOD_OVERALL,
            PERIOD_7DAYS,
            PERIOD_1MONTH,
            PERIOD_3MONTHS,
            PERIOD_6MONTHS,
            PERIOD_12MONTHS,
        ]
    ),
)
@click.option("--width", "-w", type=click.IntRange(1, 10), default=3)
@click.option("--height", "-h", type=click.IntRange(1, 10), default=3)
@click.option("--ascii", is_flag=True, default=False)
@click.option("--open", "_open", is_flag=True, default=False)
def album_grid(network, username, output, period, width, height, ascii, _open):
    im = get_cover_art_grid(network, username, period, width, height)
    if not im:
        raise click.Abort("Failed to generate image")
    if ascii:
        art = AsciiArt.from_pillow_image(im)
        art.to_terminal()
        return
    im.save(output.name, format="JPEG")
    if _open:
        startfile(output.name)

