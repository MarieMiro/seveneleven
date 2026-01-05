import os
from pathlib import Path

# Если будешь использовать DATABASE_URL (Render) — поставь пакет:
# pip install dj-database-url
try:
    import dj_database_url
except ImportError:
    dj_database_url = None

BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------
# Security
# -------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'unsafe-dev-secret-key')

DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

ALLOWED_HOSTS = os.environ.get(
    'DJANGO_ALLOWED_HOSTS',
    '127.0.0.1,localhost'
).split(',')


# Если на Render ставишь домен типа: yourapp.onrender.com
# то в переменную DJANGO_ALLOWED_HOSTS добавь его.


# -------------------------
# Application definition
# -------------------------
INSTALLED_APPS = [
    'main',
    'api.apps.ApiConfig',

    'django_bootstrap5',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_cleanup',
    'easy_thumbnails',
    'captcha',

    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Важно: CorsMiddleware должен быть выше CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # если будут общие шаблоны вне app — добавим сюда
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.middleware.bboard_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'bboard.wsgi.application'


# -------------------------
# Database
# -------------------------
# Вариант 1 (Render): DATABASE_URL есть -> используем его.
# Вариант 2 (локально): DATABASE_URL нет -> используем POSTGRES_* переменные,
# либо дефолтные значения (как у тебя).

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL and dj_database_url:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'bboard_db'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', '1'),
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }


# -------------------------
# Password validation
# -------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# -------------------------
# Internationalization
# -------------------------
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# -------------------------
# Static / Media
# -------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# -------------------------
# Auth

# -------------------------
AUTH_USER_MODEL = 'main.AdvUser'
LOGOUT_REDIRECT_URL = 'main:index'


# -------------------------
# Email (локально в консоль)
# -------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# -------------------------
# Thumbnails
# -------------------------
THUMBNAIL_ALIASES = {
    '': {
        'default': {
            'size': (96, 96),
            'crop': 'scale',
        },
    },
}
THUMBNAIL_BASEDIR = 'thumbnails'


# -------------------------
# CORS (для API)
# -------------------------
# Для учебного можно так, но в проде лучше ограничить доменами.
CORS_ALLOW_ALL_ORIGINS = True
CORS_URLS_REGEX = r'^/api/.*$'


# -------------------------
# Default PK
# -------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'