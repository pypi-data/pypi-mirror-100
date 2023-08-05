from loguru import logger

logger.add("file_{time}.log", level="TRACE", rotation="100 MB")

__author__ = "DanilaCharushin"
__version__ = "0.0.1"
__email__ = "charushin2000@gmail.com"
