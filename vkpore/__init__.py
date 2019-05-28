"""Library for interacting with Vkontakte."""

import logging

from .vkpore import Vkpore


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [ %(levelname)s ] %(message)s'
)
