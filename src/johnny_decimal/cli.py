import logging
import sys

import click

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
@click.argument('command')
@CONTEXT
def cli(ctx,
        command):
    """
    JD is a Python CLI application for creating, traversing,
    and managing a Johnny Decimals directory structure.

    Currently supports the following commands:

    - init   --> initializes a johnny decimals directory index

    WIP commands:
    
    - sync  --> syncs a target directory structure with a provided Johnny
                Decimals index
    """
    ctx.command = command





@cli.command('many')
@click.option('-i', '--index', type=str)
@click.option('-o', '--output', type=str)
@CONTEXT
def many(ctx,
         _input,
         _output,
         street,
         city,
         state,
         zipcode):
    """
    Geocode many street addresses from input and save results to output

    Input options:
    - local file
    - bigquery table

    Output options:
    - local file
    - bigquery table
    """
    provider = ctx.provider

    input_records = Input(_input,
                          street_source=street,
                          city_source=city,
                          state_source=state,
                          zipcode_source=zipcode)

    logger.info(
        'GEOCODING: %s addresses using %s geocoder:',
        len(input_records.data),
        provider)

    if provider == 'census':
        raise NotImplementedError
    elif provider == 'nominatim':
        raise NotImplementedError

    elif provider == 'smartystreets':
        smartystreets = Smartystreets(input=input_records,
                                      include_parsed_address=ctx.include_parsed_address,  # noqa: E501
                                      include_metadata=ctx.include_metadata,
                                      include_geometries=ctx.include_geo)
        smartystreets.geocode()
        report_stats(provider=provider,
                     passes=len(smartystreets.output[PASS]),
                     fails=len(smartystreets.output[FAIL]),
                     total=len(smartystreets.input_data))
        output = Output(input=smartystreets,
                        path=_output,
                        skip_upload_to_addressdb=ctx.skip_upload_to_addressdb,
                        if_table_exists_strategy=ctx.if_output_table_exists,
                        replace_addressdb_tables=ctx.replace_addressdb_tables,
                        style=ctx.output_style)
        output.save()
        logger.info('%sDONE%s', "-"*10, "-"*10)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
