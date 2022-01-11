import os

from azure_monitor.core.config import PROXY


def remove() -> None:
    os.environ.update({"http_proxy": ""})
    os.environ.update({"https_proxy": ""})


def setup() -> None:
    if PROXY:
        os.environ.update({"http_proxy": PROXY})
        os.environ.update({"https_proxy": PROXY})
