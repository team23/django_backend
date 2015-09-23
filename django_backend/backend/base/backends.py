from django_viewset import URLView

from django_backend.forms import BaseBackendForm
from .. import BaseModelBackend
from .views import *


class ModelBackend(BaseModelBackend):
    '''
    Base backend class for all backends in that are used with DjangoMC.

    There are basically four different subclasses if DjangoMCBackend that can
    be used directly.

    Pages, products (i.e. full blown pages) etc should use the
    ``ComponentProviderBackend``.

    Components that are reusable will use the ``ReusableComponentBackend`` for
    the backend instance that will be shown in the sidebar and only allows the
    editing of components that are marked as reusable.

    Components also always define an inline backend which might either be
    ``InlineComponentBackend`` or ``ReusableInlineComponentBackend`` depending
    whether the component is reusable or not.
    '''

    form_class = BaseBackendForm

    index = URLView(r'^$', BackendListView)
    create = URLView(r'^add/$', BackendCreateView)
    read = URLView(r'^(?P<pk>[^/]+)/read/$', BackendReadView)
    update = URLView(r'^(?P<pk>[^/]+)/update/$', BackendUpdateView)
    delete = URLView(r'^(?P<pk>[^/]+)/delete/$', BackendDeleteView)

    select = URLView(r'^select/$', BackendSelectView)
