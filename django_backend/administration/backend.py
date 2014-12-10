from .. import site, Group
from .backends import AdministrationBackend
from django.utils.translation import ugettext_lazy as _


account_backend = site.register(
    AdministrationBackend,
    registry='inline',
    id='administration'
)
