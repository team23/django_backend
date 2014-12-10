from django_viewset import URLView
from ..backend import BaseBackend
from .views import AdministrationView, PasswordChangeView


class AdministrationBackend(BaseBackend):
    index = URLView(r'^$', AdministrationView)
    password_change = URLView(r'^password_change/$', PasswordChangeView)
