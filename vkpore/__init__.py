"""Library for interacting with Vkontakte."""

import logging

from .vkpore import Vkpore
from .vkclient import VkClient


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [ %(levelname)s ] %(message)s'
)
