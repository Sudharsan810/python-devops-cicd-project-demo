import logging
from collections.abc import Collection

import click

from .checker import check_urls

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-6s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@click.command()
@click.argument("urls", nargs=-1)
@click.option("--timeout", default=5, help="timeout in sec for each request")
@click.option("--verbose", "-v", is_flag=True, help="enable debug logging")
def main(urls: Collection, timeout: int, verbose: bool):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("logging level set to Debug")

    if not urls:
        logger.warning("No urls provided")
        click.echo("Usage: check-urls <URL1> <URL2> ...")
        return

    logger.info(f"urls: {urls}")
    logger.info(f"timeout: {timeout}")
    logger.info(f"verbose: {verbose}")

    results = check_urls(urls, timeout)

    click.echo("\n-------Results---------\n")

    for url, status in results.items():
        if "OK" in status:
            fg_color = "green"
        else:
            fg_color = "red"
        click.secho(f"{url} -> {status}", fg=fg_color)
