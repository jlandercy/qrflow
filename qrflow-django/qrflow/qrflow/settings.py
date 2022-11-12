import os
import secrets
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("APP_SECRET_KEY", "2900a0f58e003aa8fbed4a1c69848e6889c88e7e098c691fea34c7d78f531887") #, secrets.token_hex(64))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv("APP_DEBUG_MODE", "1")))

ALLOWED_HOSTS = ["localhost", os.getenv("APP_ALLOWED_HOST", "qrflow.com")]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third parties:
    'bootstrap5',
    'crispy_forms',
    "crispy_bootstrap5",
    # Project:
    'core',
    'pki'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'qrflow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["qrflow/templates"],
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

WSGI_APPLICATION = 'qrflow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("APP_DATABASE_NAME", "qrflow"),
        'USER': os.getenv("APP_DATABASE_USER", "qrflow"),
        'PASSWORD': os.getenv("APP_DATABASE_PASSWORD", "qrflow"),
        'HOST': os.getenv("APP_DATABASE_HOST", "localhost"),
        'PORT': os.getenv("APP_DATABASE_PORT", 5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


URL_PREFIX = os.getenv("APP_URL_PREFIX", "")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = URL_PREFIX + 'static/'
STATIC_ROOT = os.getenv("APP_STATIC_ROOT", BASE_DIR / 'static')

STATICFILES_DIRS = [
    BASE_DIR / 'qrflow/static'
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = URL_PREFIX + 'media/'
MEDIA_ROOT = os.getenv("APP_MEDIA_ROOT", BASE_DIR / 'media')

# https://stackoverflow.com/questions/9692625/csrf-verification-failed-request-aborted-on-django
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "https://landercy.be"]
#CSRF_COOKIE_DOMAIN = os.getenv("APP_ALLOWED_HOST", "landercy.be")

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"


AUTH_USER_MODEL = "core.CustomUser"  # new

