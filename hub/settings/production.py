import sys
sys.path.append('/usr/src/app')

from hub.settings.base import *
import os

DEBUG = os.getenv('DEBUG', 'Secret key not found!!')    # add to env variables

ALLOWED_HOSTS = ['*']

## DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'cloud-db', 
        # 'USER': os.getenv('POSTGRES_USER', 'no postgres_user'), 
        # 'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'no postgres password'), 
        # 'HOST': os.getenv('POSTGRES_HOST', 'no host set'), 
        # 'PORT': os.getenv('POSTGRES_PORT', 'no port set'),
    }
}

redis_port = os.getenv('REDIS_PORT', 'redis port not found')               # add to env variables
redis_host = os.getenv('REDIS_HOST', 'redis host not found')               # add to env variables
redis_pass = os.getenv('REDIS_PASSWORD', 'redis password not found')       # add to env variables
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://:{redis_pass}@{redis_host}:{redis_port}/1",
        "OPTIONS": {
            # "PASSWORD" : redis_pass,
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "caching"
    }
}


# Celery Configs(local)
CELERY_BROKER_URL = f'redis://:{redis_pass}@{redis_host}:{redis_port}/0'
CELERY_RESULT_BACKEND = f'redis://:{redis_pass}@{redis_host}:{redis_port}/0'

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
            "hosts": [f'redis://:{redis_pass}@{redis_host}:{redis_port}/2'],
        },
    },
}


#* Password validation
# Password validation
from django.contrib.auth.password_validation import (
                                                    UserAttributeSimilarityValidator, MinimumLengthValidator, 
                                                    CommonPasswordValidator, NumericPasswordValidator
                                                    )
from validation.validators import (
                                    NumberValidator, UppercaseValidator, SymbolValidator
                                    )

AUTH_PASSWORD_VALIDATORS_LIST = [UserAttributeSimilarityValidator, MinimumLengthValidator, 
                                CommonPasswordValidator, NumericPasswordValidator,
                                NumberValidator, UppercaseValidator, SymbolValidator]


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'validation.validators.NumberValidator',
    },
    {
        'NAME': 'validation.validators.UppercaseValidator',
    },
    {
        'NAME': 'validation.validators.SymbolValidator',
    }
]

#* COR-HEADER SETTINGS
CORS_ALLOWED_ORIGINS = [
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]


#* Timestamp(seconds) for PasswordResetTokenGenerator (default is 7 days)
PASSWORD_RESET_TIMEOUT_DAYS = 7


## EMAIL CONFIGURATION
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST=os.getenv('EMAIL_HOST', 'EMAIL_HOST not found')                                # add to env variables
EMAIL_PORT=587
EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER', 'EMAIL_HOST_USER not found')                 # add to env variables
EMAIL_HOST_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD', 'EMAIL_HOST_PASSWORD not found')     # add to env variables
EMAIL_USE_TLS=True
