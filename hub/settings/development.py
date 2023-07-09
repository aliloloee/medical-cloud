from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

## Database(s)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hub',
        'USER': 'postgres', 
        'PASSWORD': 'ali90055',
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}


# CACHE
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "caching"
    }
}

# Celery Configs(local)
CELERY_BROKER_URL = f'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = f'redis://127.0.0.1:6379/0'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json', ]
CELERY_RESULT_EXPIRES = timedelta(days=1)
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_ALWAYS_EAGER = False
CELERY_WORKER_PREFETCH_MULTIPLIER = 4


# CHANNELS LAYER
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


# COR-HEADER SETTINGS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:0000",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]


## Timestamp(seconds) for PasswordResetTokenGenerator (default is 7 days)
PASSWORD_RESET_TIMEOUT = 60*60 # 1hour

# MINUMUM SECONDS FOR PILL ALARM SETTING
PILL_ALARM_MIN_INTERVAL = 1   # ONE SECOND

## EMAIL CONFIGURATION
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST_USER = 'info@gmail.com'


