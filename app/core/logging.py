import sys
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings

from app.core.config import settings


class LogConfig(BaseSettings):
    LEVEL: str = "INFO"
    CONSOLE_FORMAT: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <4}</level> |"
        " <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> -"
        " <level>{message}</level>"
    )
    FILE_FORMAT: str = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} |"
        " {message}"
    )
    JSON_FORMAT: str = (
        '{{"time":"{time:YYYY-MM-DD'
        ' HH:mm:ss.SSS}","level":"{level}","name":"{name}","function":"{function}","line":"{line}","message":"{message}"}}'
    )
    FILE_PATH: Path = Path(f"{settings.PROJECT_ROOT_DIRECTORY}/app/logs/app.log")
    JSON_PATH: Path = Path(f"{settings.PROJECT_ROOT_DIRECTORY}/app/logs/app.json")
    ROTATION: str = "100 MB"
    RETENTION: str = "30 days"
    COMPRESSION: str = "gz"
    ENQUEUE: bool = True

    class Config:
        env_prefix = "LOG_"


class AppLogger:
    def __init__(self):
        self.config = LogConfig()
        self.setup()

    def setup(self):
        logger.remove()  # Remove default handler

        # Console handler
        logger.add(
            sys.stdout,
            format=self.config.CONSOLE_FORMAT,
            level=self.config.LEVEL,
            enqueue=self.config.ENQUEUE,
        )

        # File handler
        logger.add(
            self.config.FILE_PATH,
            format=self.config.FILE_FORMAT,
            level=self.config.LEVEL,
            rotation=self.config.ROTATION,
            retention=self.config.RETENTION,
            compression=self.config.COMPRESSION,
            enqueue=self.config.ENQUEUE,
        )

        # JSON file handler
        logger.add(
            self.config.JSON_PATH,
            format=self.config.JSON_FORMAT,
            level=self.config.LEVEL,
            rotation=self.config.ROTATION,
            retention=self.config.RETENTION,
            compression=self.config.COMPRESSION,
            serialize=True,
            enqueue=self.config.ENQUEUE,
        )

    def get_logger(self, name: str = None):
        return logger.bind(module=name) if name else logger


logger = AppLogger()
