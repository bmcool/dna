
from defaults import *

DEBUG = TEMPLATE_DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_ROOT, "database", "test.db"),
    }
}
