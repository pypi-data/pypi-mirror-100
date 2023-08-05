from loguru import logger

logger.add("trace_{time}.log", level="TRACE", rotation="100 MB")

__all__ = ["logger"]

__author__ = "DanilaCharushin"
__version__ = "0.0.1"
__email__ = "charushin2000@gmail.com"
