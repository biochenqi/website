import pymysql

from .base import *  # NOQA
from sysucc.settings import get_env


envd = get_env()

SECRET_KEY = envd.get('SK')

DEBUG = False

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

EMAIL_HOST_USER = envd.get('EHU')
EMAIL_HOST_PASSWORD = envd.get('EHP')

# 日志文件
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s %(levelname)s %(module)s] %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s %(levelname)s %(module)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default',
            'filename': os.path.join(BASE_DIR, 'log', 'info.log'),  # replace
            'when': 'D',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'myproject': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
