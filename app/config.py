import os
import sys

from dotenv import load_dotenv
from dynaconf import LazySettings
from loguru import logger

logger.remove()
logger.add(sys.stderr, level='INFO', colorize=False)

load_dotenv('.env')
logger.info('loaded .env')

if os.environ.get('ENV') is not None:
    load_dotenv(os.environ.get('ENV') + '.env', override=True)
    if os.environ.get('ENV') == 'local':
        logger.info(f'swagger http://{os.environ.get("APP_HOST")}:{os.environ.get("APP_PORT")}/docs')
    logger.info(f'loaded {os.environ.get("ENV")}.env')

settings = LazySettings(ENVVAR_PREFIX_FOR_DYNACONF=False)

if not hasattr(settings, 'ENV'):
    settings.ENV = ''

logger.remove()
logger.add(sys.stderr, level=settings.LOG_LEVEL, colorize=False)
