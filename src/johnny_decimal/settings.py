from johnny_decimal.utils import load_env

load_env()

# general settings
LOGGING_FORMAT = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"  # noqa: E501
LOGGING_DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p'
LOGGING_FILE = 'log.txt'
