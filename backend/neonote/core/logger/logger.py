import logging
from neonote.core.logger.config_logger import setup_logger
from neonote.core.config import settings

setup_logger(log_level=settings.LOG_LEVEL, log_path=settings.LOG_PATH)

logger = logging.getLogger("app")
