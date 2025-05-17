import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'clave-temporal-para-desarrollo'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS = [
    'main',
    'django_extensions'
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'