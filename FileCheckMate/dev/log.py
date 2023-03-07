import os
import logging.config
from pathlib import Path

log_folder = Path(__file__).parent.parent.parent / "logs"
log_folder.mkdir(exist_ok=True)
log_file = log_folder / "monitor.log"
if not log_file.exists():
    log_file.touch()

base_dir = os.path.abspath(os.path.dirname(__file__))
logs_target = os.path.abspath(os.path.join(base_dir, "../../logs/monitor.log"))

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "class": "logging.Formatter",
            "format": "%(asctime)s %(message)s",
            "datefmt": "%d %b %y %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": "INFO",
            "filename": logs_target,
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 1048576,
            "backupCount": 10
        }
    },
    "loggers": {
        "FileCheckMate": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
