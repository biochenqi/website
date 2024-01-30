import pymysql

from .base import *  # NOQA
from sysucc.settings import get_env


envd = get_env()

SECRET_KEY = envd.get('SK')

ALLOWED_HOSTS = envd.get('AH')

pymysql.install_as_MySQLdb()
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": 'sysucc_db',
        'USER': envd.get('DDU'),
        'PASSWORD': envd.get('DDP'),
        'HOST': 'localhost',
        'PORT': 3306,
    },
}

MEDIA_ROOT = envd.get('MR')

# for test
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(MEDIA_ROOT, "db.sqlite3"),
#     }
# }

EMAIL_HOST_USER = envd.get('EHU')
EMAIL_HOST_PASSWORD = envd.get('EHP')
