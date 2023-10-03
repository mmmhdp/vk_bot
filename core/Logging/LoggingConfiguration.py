import logging.config
from decouple import config


class LoggingConfiguration:
    LOG_FILENAME = config("LOG_FILENAME")
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "default": {
                "format": "%(levelname)s - %(asctime)s - %(process)d - %(message)s  - %(name)s - %(lineno)d",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },

        "handlers": {
            "logfile": {
                "formatter": "default",
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_FILENAME,
                "backupCount": 2,
            },
        },

        "loggers": {
        },

        "root": {
            "level": "INFO",
            "handlers": [
                "logfile",
            ]
        },
    }

    @classmethod
    def activate_config_for_logger(cls):
        logging.config.dictConfig(cls.LOGGING_CONFIG)
