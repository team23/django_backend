from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .autoload import autoload_backends


class DjangoBackendConfig(AppConfig):
    name = 'django_backend'
    verbose_name = _('Backend')

    def ready(self):
        autoload_backends()
