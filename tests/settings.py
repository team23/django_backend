import os
import warnings
warnings.simplefilter('always')

test_dir = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

USE_I18N = True
USE_L10N = True

INSTALLED_APPS = [
    'django_backend',
    'django_callable_perms',
    'django_superform',
    'django_viewset',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'floppyforms',
    'tests',
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MIDDLEWARE_CLASSES = ()

AUTHENTICATION_BACKENDS = (
    'django_callable_perms.backends.CallablePermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_DIRS = (
    os.path.join(test_dir, 'templates'),
)

STATIC_URL = '/static/'

SECRET_KEY = '0'

SITE_ID = 1
