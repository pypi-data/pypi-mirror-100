import copy
import logging
from typing import Dict

from django.conf import settings

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = {"RAISE_PYTHON_EXCEPTION": False}


def get_settings() -> Dict:
    pretty_exeption_handler_settings = copy.deepcopy(DEFAULT_SETTINGS)
    user_settings = {
        x: y
        for x, y in getattr(settings, "PRETTY_EXEPTION_HANDLER_SETTINGS", {}).items()
        if y is not None
    }
    pretty_exeption_handler_settings.update(user_settings)
    return pretty_exeption_handler_settings
