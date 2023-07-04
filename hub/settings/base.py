from pathlib import Path
from datetime import timedelta
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_DIR = BASE_DIR / 'templates'


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'Secret key not found!!')


# Application definition
INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # rest framework
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # cors
    'corsheaders',

    # Local
    'accounts',
    'validation',
    'profiles',
    'devices',
    'client',
    'pills',

    # Celery beat
    'django_celery_beat',

    # Swagger
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION = 'hub.wsgi.application'
ASGI_APPLICATION = 'hub.asgi.application'


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

############## ADDED ###############


# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Media
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


# REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# SWAGGER SETTINGS
SWAGGER_SETTINGS = {
    "DEFAULT_MODEL_RENDERING": "example",
    'SECURITY_DEFINITIONS': {
        'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header'
        }
    }
}

# JWT CONFIGURATION
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    'SIGNING_KEY': os.getenv('SECRET_KEY', 'Secret key not found!!'),

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',
}



############# APP Settings #############

## PROFILES
from django.utils.translation import gettext_lazy as _

# YES-NO Fields
YES = 1, _('YES')
NO  = 0, _('NO')

# Profile Types
STANDARD = 1, _('STANDARD')
PRO      = 2, _('PRO')
ADVANCED = 3, _('ADVANCED')
FREE     = 4, _('FREE')

# Gender types
MALE    = 1, _('MALE')
FEMALE  = 2, _('FEMALE')
OTHER   = 3, _('OTHER')

# Education levels
BELOW_HIGHSCHOOL  = 1, _('BELOW HIGHSCHOOL')
HIGHSCHOOL        = 2, _('HIGHSCHOOL')
ABOVE_HIGHSCHOOL  = 3, _('ABOVE HIGHSCHOOL')

# Employment status
UNEMPLOYED  = 1, _('UNEMPLOYED')
EMPLOYED    = 2, _('EMPLOYED')
RETIRED     = 3, _('RETIRED')

# Physical activity
NEVER    = 0, _('NEVER')
SELDOM   = 1, _('SELDOM')
REGULAR  = 2, _('REGULAR')

# Fruit and Vegetable consumption
LOW       = 0, _('LOW')
AVERAGE   = 1, _('AVERAGE')
HIGH      = 2, _('HIGH')

# Obesity
THIN               = 1, _('THIN')
FIT                = 2, _('FIT')
OVERWEIGHT         = 3, _('OVERWEIGHT')
EXTREME_OVERWEIGHT = 4, _('EXTREME OVERWEIGHT')

## DEVICES
# SETTING FOR CREATING API_KEY OF THE DEVICE
DEVICE_API_KEY_SETTINGS = {
    'MESSAGE_LOWER_BAND': 20,
    'MESSAGE_UPPER_BAND': 30,
    'HASHING_METHOD': 'sha3_256' # 'default' to use django make_password 
}


# MINIMUM CHARGE TO ALLOW USERS CREATE NEW DEVICE
MINIMUM_CHARGE_FOR_CREATE_NEW_DEVICE = 50000

# LIMITATIONS (MAXIMUM NUMBER OF DEVICES)
MAX_NOD = {
    'STANDARD' : 1,
    'PRO' : 5,
    'ADVANCED' : 20,
    'FREE' : -1
}

# DEVICE ACTIVATION CODE LENGTH
DEV_CODE_LENGTH = 4

# DEVICE ACTIVATION CODE EXPIRATION TIMESTAMP
DEVICE_ACTIVATION_CODE_EXPIRATION_TIMESTAMP = 3*60

# DEVICE HEADER NAME FOR ACCEPTING REQUESTS TO CREATE DATA
DEVICE_HEADER_NAME = 'DEVICE_AUTHORIZATION'
DEVICE_HEADER_RECORD_NAME = 'name'
DEVICE_HEADER_NAME_WS = 'device'
DEVICE_HEADER_TYPES = ('Avian', )



## RECORDS
ALLOWED_FILE_CONTENT_TYPES = ('text/csv', ) 
