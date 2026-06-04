from pathlib import Path
from decouple import config
import os
import cloudinary
from dotenv import load_dotenv
load_dotenv()  

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG      = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS        = ['127.0.0.1', 'localhost', 'photoghor.onrender.com']
CSRF_TRUSTED_ORIGINS = ['https://photoghor.onrender.com', 'http://127.0.0.1:8000']

# =========================================================
# INSTALLED APPS
# =========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',          # must be BEFORE staticfiles
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'cloudinary',
    'photoshop',
]

# =========================================================
# CLOUDINARY  (configure once, here)
# =========================================================

cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key   =config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET'),
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY'   : config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}

# =========================================================
# MIDDLEWARE  (defined ONCE)
# =========================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # right after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

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

WSGI_APPLICATION = 'PHOTOGHOR.wsgi.application'

# =========================================================
# DATABASE
# =========================================================

if os.environ.get('DJANGO_ENV') == 'production':
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME'  : BASE_DIR / 'db.sqlite3',
        }
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


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Intha context-la staticfiles storage path romba mukkiyam
# இப்படி மாத்துங்கள்
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# MEDIA_ROOT is only used for local dev fallback; Cloudinary ignores it.
MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# settings.py
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# =========================================================
# AUTH BACKENDS
# =========================================================

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_URL           = '/'
LOGIN_REDIRECT_URL  = '/live_preview/'
LOGOUT_REDIRECT_URL = '/live_preview'

SITE_ID = 1

# =========================================================
# ALLAUTH SETTINGS
# =========================================================

ACCOUNT_UNIQUE_EMAIL       = True
ACCOUNT_LOGIN_METHODS      = {'email'}
ACCOUNT_SIGNUP_FIELDS      = ['email*', 'password1*', 'password2*']
SOCIALACCOUNT_AUTO_SIGNUP  = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_ADAPTER      = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'

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
        'SCOPE'      : ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

ACCOUNT_DEFAULT_HTTP_PROTOCOL      = 'http'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# =========================================================
# SECURITY  (tighten these when you add HTTPS)
# =========================================================

SECURE_SSL_REDIRECT            = False
SECURE_HSTS_SECONDS            = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD            = False