from django.views.generic import UpdateView

from .edit import BackendFormViewMixin


class BackendReadView(BackendFormViewMixin, UpdateView):
    http_method_names = ['get']
    template_type = 'read'

    def get_required_object_permissions(self):
        return super(BackendReadView, self).get_required_object_permissions() + ['read']

    def get_context_data(self, **kwargs):
        kwargs.setdefault('readonly', True)
        return super(BackendReadView, self).get_context_data(**kwargs)
