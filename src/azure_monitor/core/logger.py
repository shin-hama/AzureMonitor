import logging
import logging.handlers

from azure_monitor.core.config import DEBUG


def setup_logger(name: str) -> None:
    """Setup logging config

    Parameter
    ---------
    name: str
        The logger name, expected root package name.
        ex) Call from __init__.py at the root of this package as `setup_logger(__name__)`.
    """
    logger = logging.getLogger(name)
    if DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    sh = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.debug("Setup Logger")
