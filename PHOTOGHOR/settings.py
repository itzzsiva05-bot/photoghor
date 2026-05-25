# =========================================================
# PHOTOGHOR/settings.py
# FULL CORRECT CODE
# =========================================================

from pathlib import Path
import os

from decouple import config, Csv
from dotenv import load_dotenv


# =========================================================
# BASE DIRECTORY
# =========================================================
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# LOAD ENV FILE
# =========================================================
load_dotenv(os.path.join(BASE_DIR, '.env'))


# =========================================================
# SECURITY
# =========================================================
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-change-this-key'
)

DEBUG = config(
    'DEBUG',
    default=True,
    cast=bool
)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='127.0.0.1,localhost',
    cast=Csv()
)


# =========================================================
# INSTALLED APPS
# =========================================================
INSTALLED_APPS = [

    # DJANGO APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # DJANGO ALLAUTH
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # YOUR APP
    'photoshop',
]


# =========================================================
# MIDDLEWARE
# =========================================================
MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    # WHITENOISE
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # ALLAUTH
    'allauth.account.middleware.AccountMiddleware',
]


# =========================================================
# ROOT URL CONFIG
# =========================================================
ROOT_URLCONF = 'PHOTOGHOR.urls'


# =========================================================
# TEMPLATES
# =========================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# =========================================================
# WSGI
# =========================================================
WSGI_APPLICATION = 'PHOTOGHOR.wsgi.application'


# =========================================================
# DATABASE
# =========================================================
DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =========================================================
# PASSWORD VALIDATORS
# =========================================================
AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)


# =========================================================
# MEDIA FILES
# =========================================================
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# =========================================================
# DEFAULT AUTO FIELD
# =========================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================================================
# SITE ID
# =========================================================
SITE_ID = 1


# =========================================================
# AUTHENTICATION BACKENDS
# =========================================================
AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',
]


# =========================================================
# LOGIN / LOGOUT REDIRECT
# =========================================================
LOGIN_REDIRECT_URL = '/live-preview/'

LOGOUT_REDIRECT_URL = '/'


# =========================================================
# DJANGO ALLAUTH SETTINGS
# =========================================================

# LOGIN USING EMAIL
ACCOUNT_LOGIN_METHODS = {'email'}

# SIGNUP FIELDS
ACCOUNT_SIGNUP_FIELDS = [
    'email*',
    'password1*',
    'password2*',
]

# EMAIL SETTINGS
ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_EMAIL_VERIFICATION = 'none'

# AUTO LOGIN AFTER GOOGLE LOGIN
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_AUTO_SIGNUP = True


# =========================================================
# GOOGLE LOGIN SETTINGS
# =========================================================
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv("GOOGLE_CLIENT_ID"),
            'secret': os.getenv("GOOGLE_CLIENT_SECRET"),
            'key': '',
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


# =========================================================
# EMAIL SETTINGS
# =========================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = config(
    'EMAIL_HOST_USER',
    default=''
)

EMAIL_HOST_PASSWORD = config(
    'EMAIL_HOST_PASSWORD',
    default=''
)