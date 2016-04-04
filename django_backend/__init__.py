from .backend.renderable import Renderable  # noqa
from .group import Group  # noqa
from .sitebackend import SiteBackend


__version__ = '0.6.0'


default_app_config = 'django_backend.apps.DjangoBackendConfig'


site = SiteBackend(id='backend')
