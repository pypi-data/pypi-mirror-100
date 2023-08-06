import logging
from logging import NullHandler

from .client import Client

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())

__version__ = '0.1.1'
