# =========================================================
# settings.py  –  PHOTOGHOR
# =========================================================

from pathlib import Path
from decouple import config
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=True, cast=bool)



ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'photoghor.onrender.com']

CSRF_TRUSTED_ORIGINS = ['https://photoghor.onrender.com']


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
    'django.contrib.sites',
    # third-party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'cloudinary_storage',
    'cloudinary',

    # local
    'photoshop',
]
import cloudinary
cloudinary.config(
    cloud_name = config('CLOUDINARY_CLOUD_NAME'),
    api_key    = config('CLOUDINARY_API_KEY'),
    api_secret = config('CLOUDINARY_API_SECRET'),
)

# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
        'DIRS': [BASE_DIR / 'templates'],
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


# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = 'PHOTOGHOR.wsgi.application'


# =========================================================
# DATABASE
# =========================================================

DATABASES = {
    'default': dj_database_url.config(
        default=config(
            'DATABASE_URL',
            default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'
        )
    )
}


# =========================================================
# PASSWORD VALIDATORS
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]


# =========================================================
# LANGUAGE & TIMEZONE
# =========================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Kolkata'
USE_I18N      = True
USE_TZ        = True


# =========================================================
# STATIC & MEDIA FILES
# =========================================================

STATIC_URL      = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT     = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# =========================================================
# DEFAULT AUTO FIELD
# =========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================================================
# AUTH BACKENDS
# =========================================================

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',           # username/password
    'allauth.account.auth_backends.AuthenticationBackend', # google oauth
]


# =========================================================
# LOGIN / LOGOUT REDIRECTS
# FIX: LOGIN_URL → '/' (உங்க custom login page)
# =========================================================

LOGIN_URL          = '/'              # custom login (index view)
LOGIN_REDIRECT_URL = '/live_preview/' # after login → live_preview
LOGOUT_REDIRECT_URL = '/live_preview'            # after logout → login page


# =========================================================
# SITES
# =========================================================

SITE_ID = 1


# =========================================================
# ALLAUTH SETTINGS
# =========================================================

ACCOUNT_UNIQUE_EMAIL    = True
ACCOUNT_LOGIN_METHODS   = {'email'}
ACCOUNT_SIGNUP_FIELDS   = ['email*', 'password1*', 'password2*']

SOCIALACCOUNT_AUTO_SIGNUP  = True
SOCIALACCOUNT_LOGIN_ON_GET = True

# Google OAuth redirect after login → live_preview
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'


# =========================================================
# GOOGLE OAUTH
# =========================================================

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret'   : config('GOOGLE_CLIENT_SECRET'),
            'key'      : '',
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    }
}

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# =========================================================
# SECURITY (Production-ல மட்டும் True பண்ணுங்க)
# =========================================================

SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

  