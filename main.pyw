import logging
import os
import sys
import subprocess
import time

subprocess.call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

from src.search import SearchWindow
from src.defines import VERSION

# TODO: update check and notification?

if __name__ == "__main__":
    logger = logging.getLogger("utdemofinder")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(module)s | %(message)s")

    loglvl = logging.INFO
    if "--debug" in sys.argv:
        loglvl = logging.DEBUG

    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = logging.FileHandler(
        f"logs/utdemofinder_{time.asctime().replace(':','-').replace(' ','_')}.log"
    )
    file_handler.setLevel(loglvl)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(loglvl)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    logger.setLevel(loglvl)

    logger.info(f"Starting new instance of utdemofinder (version: {VERSION})")

    _ = SearchWindow()
