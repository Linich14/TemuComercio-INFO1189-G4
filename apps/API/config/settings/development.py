"""
Development settings - Open/Closed principle
Extends base settings without modifying them
"""
import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database for development - using Supabase PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('SUPABASE_DB_NAME'),
        'USER': os.getenv('SUPABASE_DB_USER'),
        'PASSWORD': os.getenv('SUPABASE_DB_PASSWORD'),
        'HOST': os.getenv('SUPABASE_DB_HOST'),
        'PORT': os.getenv('SUPABASE_DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Fallback to SQLite if Supabase credentials are not provided
if not all([
    os.getenv('SUPABASE_DB_NAME'),
    os.getenv('SUPABASE_DB_USER'),
    os.getenv('SUPABASE_DB_PASSWORD'),
    os.getenv('SUPABASE_DB_HOST')
]):
    print("⚠️  Supabase credentials not found, falling back to SQLite for development")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Development-specific middleware
MIDDLEWARE += [
    # Add any development-specific middleware here
]

# Development-specific apps
INSTALLED_APPS += [
    # Add development tools like django-debug-toolbar
]

# Email backend for development (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# CORS settings for development (if needed)
CORS_ALLOW_ALL_ORIGINS = True