# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#
import logging
import os
from datetime import timedelta
from typing import Optional

from cachelib.file import FileSystemCache
from celery.schedules import crontab

logger = logging.getLogger()


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)

LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "ru": {"flag": "ru", "name": "Russian"},
}

# Keycloak
from keycloak_security_manager import  OIDCSecurityManager
from flask_appbuilder.security.manager import AUTH_OID
import os
curr  =  os.path.abspath(os.getcwd())
AUTH_TYPE = AUTH_OID
OIDC_CLIENT_SECRETS =  curr + '/docker/pythonpath_dev/client_secret.json'
OIDC_ID_TOKEN_COOKIE_SECURE = False
OIDC_REQUIRE_VERIFIED_EMAIL = False
OIDC_OPENID_REALM: 'MIEM'
OIDC_INTROSPECTION_AUTH_METHOD: 'client_secret_post'
CUSTOM_SECURITY_MANAGER = OIDCSecurityManager
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = 'Gamma'
OIDC_VALID_ISSUERS = ['https://profile.miem.hse.ru/auth/realms/MIEM']
    
# Sentry
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

# sentry_sdk.init(
#     dsn=get_env_variable("SENTRY_DSN"),
#     integrations=[FlaskIntegration()],
#     traces_sample_rate=1.0
# )

EXTRA_CATEGORICAL_COLOR_SCHEMES = [
    {
        'id': 'hseColors',
        'label': 'HSE Colors',
        'colors': [
            '#11A0D7',
            '#EB8C3C',
            '#47A0A0',
            '#FBBA00',
            '#96628C',
            '#CD5A5A',
            '#7DA0D3',
            '#47A0A0',
            '#029C63',
            '#D7EBB4',
            '#FFDC91',
            '#FFF07D',
            '#FFD746'
        ],
    },
    {
        'id': 'hseColors_shifted',
        'label': 'HSE Colors shifted',
        'colors': [
            '#EB8C3C',
            '#47A0A0',
            '#FBBA00',
            '#96628C',
            '#CD5A5A',
            '#7DA0D3',
            '#47A0A0',
            '#029C63',
            '#D7EBB4',
            '#FFDC91',
            '#FFF07D',
            '#FFD746',
            '#11A0D7'
        ],
    },
    {
        'id': 'hseColors_green',
        'label': 'HSE Colors green',
        'colors': [
            '#029C63',
            '#47A0A0',
            '#FBBA00',
            '#96628C',
            '#CD5A5A',
            '#7DA0D3',
            '#47A0A0',
            '#EB8C3C',
            '#D7EBB4',
            '#FFDC91',
            '#FFF07D',
            '#FFD746',
            '#11A0D7'
        ],
    },
]


DATABASE_DIALECT = get_env_variable("DATABASE_DIALECT")
DATABASE_USER = get_env_variable("DATABASE_USER")
DATABASE_PASSWORD = get_env_variable("DATABASE_PASSWORD")
DATABASE_HOST = get_env_variable("DATABASE_HOST")
DATABASE_PORT = get_env_variable("DATABASE_PORT")
DATABASE_DB = get_env_variable("DATABASE_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
    DATABASE_DIALECT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DB,
)

REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")
REDIS_CELERY_DB = get_env_variable("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = get_env_variable("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

CACHE_CONFIG = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 3600,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG

FILTER_STATE_CACHE_CONFIG = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 3600,
    "CACHE_KEY_PREFIX": "superset_state_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}

EXPLORE_FORM_DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 3600,
    "CACHE_KEY_PREFIX": "superset_form_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}

class CeleryConfig(object):
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = ("superset.sql_lab",)
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
        'cache-warmup-daily': {
                'task': 'cache-warmup',
                'schedule': crontab(minute=0, hour=7),
                'kwargs': {
                    'strategy_name': 'top_n_dashboards',
                    'top_n': 20,
                    'since': '3 days ago',
                },
        },
    }


CELERY_CONFIG = CeleryConfig

FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "EMBEDDED_SUPERSET": True,
    "DASHBOARD_RBAC": True,
    "HORIZONTAL_FILTER_BAR": True,
    "DRILL_TO_DETAIL": True,
    "DASHBOARD_CROSS_FILTERS": True
}

# FEATURE_FLAGS = {
#     "ALERT_REPORTS": True,
#     "EMBEDDED_SUPERSET": True,
#     "DASHBOARD_RBAC": True
# }
GUEST_ROLE_NAME = "public_guest"

HTTP_HEADERS = {'X-Frame-Options': 'ALLOWALL',
}

ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
WEBDRIVER_BASEURL = "https://superset:8088/"
# The base URL for the email report hyperlinks.
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL

SQLLAB_CTAS_NO_LIMIT = True

#
# Optionally import superset_config_docker.py (which will have been included on
# the PYTHONPATH) in order to allow for local settings to be overrided
#
try:
    import superset_config_docker
    from superset_config_docker import * 

    logger.info(
        f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]"
    )
except ImportError:
    logger.info("Using default Docker config...")
