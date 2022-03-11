import logging
from pathlib import Path

import pytoml as toml


class DirectoryMixin:

    def mkdir(self) -> None:
        """
        Makes a directory from the path property
        """
        logging.info("Creating directory %s", self.path)
        self.path.mkdir(parents=True, exist_ok=True)
