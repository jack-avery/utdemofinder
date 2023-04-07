import json
import logging
import os

CONFIG_PATH = "config.txt"
"""Path to the user config file to use"""

DEFAULT = {"demo_folder": False}

logger = logging.getLogger("utdemofinder")


class Config:
    """
    Configuration class for UTDemoFinder.
    """

    demo_folder: str = False
    """Demo folder"""

    def read(self):
        """
        Read from `CONFIG_PATH` and return the contained json.

        Create the file with the default if it does not exist.
        """
        logger.debug(f"reading {CONFIG_PATH}")
        if not os.path.exists(CONFIG_PATH):
            self.populate_default()
            return

        with open(CONFIG_PATH, "r") as cfgfile:
            cfg = json.loads(cfgfile.read())

        self.demo_folder = cfg["demo_folder"]

    def write(self):
        logger.debug(f"writing {CONFIG_PATH}")
        with open(CONFIG_PATH, "w") as cfgfile:
            cfgfile.write(json.dumps(self.json(), indent=4))

    def populate_default(self):
        logger.debug(f"populating default config")
        self.demo_folder = False
        self.write()

    def json(self):
        return {"demo_folder": self.demo_folder}
