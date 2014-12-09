from django.conf.urls import include, url

from django_viewset import URLView
from .backend import BaseBackend
from .views.auth import LoginView, LogoutView
from .views.index import IndexView


class SiteInlineBackends(object):
    def __init__(self, site_backend):
        self.site_backend = site_backend

    def __getitem__(self, key):
        try:
            return self.site_backend.find(id=key, registry='inline')
        except ValueError as e:
            raise KeyError(e.args[0])


class SiteBackend(BaseBackend):
    login = URLView(r'^login/$', LoginView)
    logout = URLView(r'^logout/$', LogoutView)

    index = URLView(r'^(?:(?P<site>[0-9]+)/(?P<language>[a-zA-Z_-]+)/)?$', IndexView)

    @property
    def inline_backends(self):
        return SiteInlineBackends(self)

    def get_urlname_prefix(self):
        return None

    def get_children_urls(self):
        base_urls = super(SiteBackend, self).get_children_urls()
        # Append all children under the language ID url.
        return [
            url(r'^(?P<site>[0-9]+)/(?P<language>[a-zA-Z_-]+)/', include(base_urls))
        ]
