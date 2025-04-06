"""
Django settings for geo_social project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
from confluent_kafka import Producer

import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@avra=@rp7o$9f@wk$px-_b-c5u*r($j=9a#3kf_--g2eksu!y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
DOMAIN = 'localhost:8000'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'geo_social_app'
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

ROOT_URLCONF = 'geo_social.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'geo_social.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django_cockroachdb',
        'NAME': 'geo_social_app_db',
        'USER': DB_USER,
        # 'PASSWORD': DB_PASSWORD, 
        'HOST': 'localhost',
        'PORT': '26257',
    },
    'us_read_1': {
        'ENGINE': 'django_cockroachdb',
        'NAME': 'geo_social_app_db',
        'USER': DB_USER,
        # 'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '26258',
    },
    'us_read_2': {
        'ENGINE': 'django_cockroachdb',
        'NAME': 'geo_social_app_db',
        'USER': DB_USER,
        # 'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost', 
        'PORT': '26259',
    },
    'eu_read_1': {
        'ENGINE': 'django_cockroachdb',
        'NAME': 'geo_social_app_db',
        'USER': DB_USER,
        # 'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '26260',
    },
    'eu_read_2': {
        'ENGINE': 'django_cockroachdb',
        'NAME': 'geo_social_app_db',
        'USER': DB_USER,
        # 'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '26261',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GDAL_LIBRARY_PATH = '/opt/homebrew/Cellar/gdal/3.10.2_3/lib/libgdal.dylib'
GEOS_LIBRARY_PATH = '/opt/homebrew/Cellar/geos//3.13.1/lib/libgeos_c.dylib'
