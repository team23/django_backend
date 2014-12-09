from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from .edit import BackendFormViewMixin
from .mixins import SaveInlineDoneMixin


class SaneCreateView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    # This is basically the same as django.views.generic.CreateView, but
    # skips the BaseCreateView base class. This is necessary to avoid resetting
    # self.object to None. This is essential for the backend to work.
    template_name_suffix = '_form'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SaneCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SaneCreateView, self).post(request, *args, **kwargs)


class BackendCreateView(SaveInlineDoneMixin, BackendFormViewMixin, SaneCreateView):
    action_name = 'create'
    template_type = 'create'
    success_url_name = 'read'

    def get_required_permissions(self):
        return super(BackendCreateView, self).get_required_permissions() + ['add']

    def get_origin(self, *args, **kwargs):
        return None

    def prepare_object(self, origin):
        return self.backend.model()

    def get_context_data(self, **kwargs):
        kwargs.setdefault('create', True)
        return super(BackendCreateView, self).get_context_data(**kwargs)

    def get_dismiss_url(self):
        return self.get_list_url()

    def get_success_url(self):
        if 'save_continue' in self.request.POST:
            return self.get_update_url(object=self.object)
        return self.get_list_url()
