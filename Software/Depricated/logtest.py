# old log test
import logging
from pathlib import Path

logging.basicConfig(
    filename=Path(__file__).with_name("app_log.txt"),
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

def main():
    logging.info("The program has started successfully.")
    logging.info("This is an informational message.")
    logging.debug("This is a test to see if debug if printed")

def jash():
    logging.error('Actually  HELP HELP HELP')

if __name__ == "__main__":
    main()
    jash()