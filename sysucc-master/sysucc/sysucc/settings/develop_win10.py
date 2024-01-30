from .base import *  # NOQA
from sysucc.settings import get_env


envd = get_env()

SECRET_KEY = envd.get('SK')

ALLOWED_HOSTS = envd.get('AH')

EMAIL_HOST_USER = envd.get('EHU')
EMAIL_HOST_PASSWORD = envd.get('EHP')

MEDIA_ROOT = 'D:/longrw/tmp/test_dj/sysucc-media/'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(MEDIA_ROOT, "db.sqlite3"),
    }
}
