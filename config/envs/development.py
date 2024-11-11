"""Flask Local Development Environment Configuration."""

import logging
from os import environ

from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class DevelopmentConfig(Config):
    #  Application Config
    FLASK_ENV = "development"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@127.0.0.1:5432/fsd_fund_store_1",  # pragma: allowlist secret
    )
