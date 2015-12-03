from .group import Group
from .sitebackend import SiteBackend


__version__ = '0.2.0.dev4'


default_app_config = 'django_backend.apps.DjangoBackendConfig'


site = SiteBackend(id='backend')
