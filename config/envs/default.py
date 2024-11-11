"""Flask configuration."""

import logging
from distutils.util import strtobool
from os import environ
from os import getenv
from pathlib import Path

from fsd_utils import CommonConfig
from fsd_utils import configclass


@configclass
class DefaultConfig(object):
    #  Application Config
    FLASK_ENV = CommonConfig.FLASK_ENV
    SESSION_COOKIE_NAME = environ.get("SESSION_COOKIE_NAME")
    FLASK_ROOT = str(Path(__file__).parent.parent.parent)

    # Logging
    FSD_LOG_LEVEL = logging.WARNING

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "").replace("postgres://", "postgresql://")
