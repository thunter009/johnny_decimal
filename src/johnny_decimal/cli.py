import logging
import sys

import click

from johnny_decimal.core import Area, Category, Input, Registry
from johnny_decimal.exceptions import NotDefined
from johnny_decimal.settings import LOGGING_DATE_FORMAT, LOGGING_FORMAT

LOG_PATH = '.'
FILE_NAME = __name__
logging.basicConfig(level=logging.INFO,
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

    - init  --> inits a target directory structure with a provided Johnny
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
        raise NotDefined("Area not defined")

    category_instances = []
    area_instances = []
    for area in areas:
        area_name = area.get('name')
        if not area_name:
            raise NotDefined("Area not defined")

        area_instance = Area(name=area_name, root=path)
        area_instances.append(area_instance)
        categories = area.get('category')

        if not categories:
            logger.info("Categories not defined for area: %s, skipping...",
                        area['name'])
            continue

        for category in categories:

            category_name = category.get("name")

            if not category_name:
                raise NotDefined(
                    f"Category not defined for {area} Area")

            category_instance = Category(
                name=category_name,
                area=area_instance)

            category_instances.append(category_instance)

    area_registry = Registry(areas=area_instances)
    area_registry.init()
    
    categories_registry = Registry(categories=category_instances)
    categories_registry.init()


@CONTEXT
def update(ctx,
           path):
    """
    Updates a Johnny Decimals directory so the 
    present directory and all sub-directories match the passed index. Searches for index.toml in current directory unless
    the --index option is passed.

    path (optional):
    - the directory path to initialize the JD directory index in
    """
    _input = Input(index)
    index = _input.load()
    areas = index.get('area')

    if not areas:
        raise NotDefined("Area not defined")

    holder = []
    for area in areas:
        area_name = area.get('name')
        if not area_name:
            raise NotDefined("Area not defined")

        area_instance = Area(name=area_name, root=path)
        categories = area.get('category')

        if not categories:
            logger.info("Categories not defined for area: %s, skipping...",
                        area['name'])
            continue

        for category in categories:

            category_name = category.get("name")

            if not category_name:
                raise NotDefined(
                    f"Category not defined for {area} Area")

            category_instance = Category(
                name=category_name,
                area=area_instance)

            holder.append(category_instance)

        registry = Registry(categories=holder)

    # ar = Registry(categories=holder)
    ar.init()


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
