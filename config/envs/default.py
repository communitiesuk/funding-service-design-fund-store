"""Flask configuration."""
import logging
from os import environ
from pathlib import Path

from fsd_utils import configclass


@configclass
class DefaultConfig(object):
    #  Application Config
    SECRET_KEY = environ.get("SECRET_KEY")
    SESSION_COOKIE_NAME = environ.get("SESSION_COOKIE_NAME")
    FLASK_ROOT = str(Path(__file__).parent.parent.parent)
    FLASK_ENV = environ.get("FLASK_ENV")

    # Logging
    FSD_LOG_LEVEL = logging.WARNING

    # Frontend
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
