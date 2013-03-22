import sys
import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

BOT_NAME = 'dna'

CONCURRENT_REQUESTS = 10000
CONCURRENT_REQUESTS_PER_DOMAIN = 10000

SPIDER_MODULES = [
    'collection.movie',
]

# COMMANDS_MODULE = 'collection.commands'

DOWNLOAD_DELAY = 0.5
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(PROJECT_PATH, 'logs', 'scrapy.log')

COOKIES_DEBUG = True

ITEM_PIPELINES = [
    'collection.pipelines.DjangoModelPipeline',
]

USER_AGENT = "scrapy"

# django environment setting
sys.path.append(PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")
