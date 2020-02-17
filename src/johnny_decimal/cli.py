import logging
import sys

import click
from johnny_decimal.core import Area, AreaRegistry, Input
from johnny_decimal.exceptions import AreasNotDefinedException
from johnny_decimal.settings import LOGGING_DATE_FORMAT, LOGGING_FORMAT

LOG_PATH = '.'
FILE_NAME = __name__
logging.basicConfig(level=logging.DEBUG,
                    datefmt=LOGGING_DATE_FORMAT,
                    format=LOGGING_FORMAT,
                    handlers=[
                        logging.FileHandler(
                            f"{LOG_PATH}/{FILE_NAME}.log",
                            encoding=None,
                            delay=False),
                        logging.StreamHandler()
                    ])


class Config:
    """Configuration Object"""


logger = logging.getLogger()
CONTEXT = click.make_pass_decorator(Config, ensure=True)


@click.group()
# @click.argument('command')
@CONTEXT
def cli(ctx):
    """
    JD is a Python CLI application for creating, traversing,
    and managing a Johnny Decimals directory structure.

    Currently supports the following commands:

    - init   --> initializes a johnny decimals directory index

    WIP commands:

    - sync  --> syncs a target directory structure with a provided Johnny
                Decimals index
    """
    # ctx.command = command


@cli.command('init')
@click.argument('index',
                type=click.Path(dir_okay=False,
                                writable=True,
                                resolve_path=True))
@click.option('-p', '--path',
              type=click.Path(file_okay=False,
                              writable=True,
                              resolve_path=True),
              default='.')
@CONTEXT
def init(ctx,
         index,
         path):
    """
    Initializes a Johnny Decimals directory index. Searches the current
    directory for index.toml unless the --index option is passed

    index (required):
    - the path to a valid Johnny Decimals index.toml file.

    path (optional):
    - the directory path to initialize the JD directory index in
    """
    _input = Input(index)
    index = _input.load()
    areas = index.get('area')

    if not areas:
        raise AreasNotDefinedException("Areas not properly defined in index")

    area_holder = []
    for area in areas:
        name = area.get('name')
        if not name:
            raise AreasNotDefinedException("Area name not supplied")

        import ipdb; ipdb.set_trace()
        area_holder.append(Area(name=name, root=path))

    ar = AreaRegistry(area_holder)
    ar.init()


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
