from neonote.core.logger.logger import logger
from neonote.core.db import init_db


def prestart():
    logger.info("Running prestart script...")
    init_db()
    logger.info("Prestart script completed.")


if __name__ == "__main__":
    prestart()
