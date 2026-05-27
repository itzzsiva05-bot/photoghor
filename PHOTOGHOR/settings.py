# =========================================================
# settings.py
# =========================================================

from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []


# =========================================================
# INSTALLED APPS
# =========================================================

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # SITES
    'django.contrib.sites',

    # ALLAUTH
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # GOOGLE
    'allauth.socialaccount.providers.google',

    # YOUR APP
    'photoshop',

]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

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
# ROOT URL
# =========================================================

ROOT_URLCONF = 'PHOTOGHOR.urls'


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

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

AUTH_PASSWORD_VALIDATORS = []


# =========================================================
# LANGUAGE
# =========================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = 'static/'


# =========================================================
# DEFAULT AUTO FIELD
# =========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# =========================================================
# AUTH BACKENDS
# =========================================================

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',

]


# =========================================================
# LOGIN REDIRECT
# =========================================================

LOGIN_REDIRECT_URL = '/live_preview/'
LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_AUTO_SIGNUP = True

SITE_ID = 1



# =========================================================
# GOOGLE LOGIN
# =========================================================

SOCIALACCOUNT_PROVIDERS = {

    'google': {

        'APP': {

            'client_id': config('GOOGLE_CLIENT_ID'),

            'secret': config('GOOGLE_CLIENT_SECRET'),

            'key': '',
        },

        'SCOPE': [
            'profile',
            'email',
        ],

        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    }
}

# settings.py

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'