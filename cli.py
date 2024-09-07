import os
import click
from pylast import LastFMNetwork
from commands import images


@click.group("lastfm-tools")
@click.pass_context
def lastfm_tools_cli(ctx):
    ctx.obj = LastFMNetwork(api_key=os.getenv("API_KEY"))


lastfm_tools_cli.add_command(images.album_grid)


if __name__ == "__main__":
    lastfm_tools_cli()
