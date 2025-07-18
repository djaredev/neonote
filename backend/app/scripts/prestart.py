from app.core.logger import logger
from app.core.db import init_db


def main():
    init_db()


if __name__ == "__main__":
    logger.info("Running prestart script...")
    main()
    logger.info("Prestart script completed.")
