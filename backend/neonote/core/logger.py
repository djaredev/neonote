import logging
import logging.config
from neonote.core.config import settings


class CustomFormatter(logging.Formatter):
    # ANSI Colors

    COLORS = {
        "DEBUG": "\033[1;30;46m",  # Cyan
        "INFO": "\033[1;30;42m",  # Green
        "WARNING": "\033[1;30;43m",  # Yellow
        "ERROR": "\033[1;30;41m",  # Red
        "CRITICAL": "\033[1;30;45m",  # Purple
    }

    # Additional codes for specific elements
    RESET = "\033[0m"  # Reset color
    BOLD = "\033[1m"
    TIMESTAMP_COLOR = "\033[90m"  # Gray
    NAME_COLOR = "\033[94m"  # Blue

    def __init__(self, fmt=None, datefmt=None, use_colors=True):
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors

    # Override format
    def format(self, record):
        if not self.use_colors:
            return super().format(record)

        record_copy = logging.LogRecord(
            record.name,
            record.levelno,
            record.pathname,
            record.lineno,
            record.msg,
            record.args,
            record.exc_info,
            record.funcName,
            record.stack_info,
        )

        level_color = self.COLORS.get(record.levelname, "")

        record_copy.levelname = f"{level_color}{record.levelname}{self.RESET}"
        record_copy.name = f"{self.NAME_COLOR}{record.name}{self.RESET}"

        if hasattr(record_copy, "asctime"):
            record_copy.asctime = (
                f"{self.TIMESTAMP_COLOR}{record_copy.asctime}{self.RESET}"
            )

        formatted = super().format(record_copy)

        return formatted

    # Override formatTime to add color
    def formatTime(self, record, datefmt=None):
        timestamp = super().formatTime(record, datefmt)
        if self.use_colors:
            return f"{self.TIMESTAMP_COLOR}{timestamp}{self.RESET}"
        return timestamp


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "()": CustomFormatter,
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M",
            "use_colors": False,
        },
        "standard_color": {
            "()": CustomFormatter,
            "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "level": settings.LOG_LEVEL,
            "formatter": "standard",
            "filename": f"{settings.LOG_PATH}",
            "mode": "a",
            "encoding": "utf-8",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": settings.LOG_LEVEL,
            "formatter": "standard_color",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("app")
