from django.views.generic import UpdateView

from .edit import BackendFormViewMixin
from .mixins import SaveInlineDoneMixin


class BackendUpdateView(SaveInlineDoneMixin, BackendFormViewMixin, UpdateView):
    action_name = 'update'
    template_type = 'update'

    def get_required_object_permissions(self):
        return super(BackendUpdateView, self).get_required_object_permissions() + ['change']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BackendUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BackendUpdateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.setdefault('update', True)
        return super(BackendUpdateView, self).get_context_data(**kwargs)

    def dismiss(self, request, *args, **kwargs):
        if self.is_dialog():
            json_data = self.get_dismiss_json()
            return self.render_json_response(json_data)
        return super(BackendUpdateView, self).dismiss(request, *args, **kwargs)

    def get_dismiss_url(self):
        return self.get_read_url(object=self.origin)

    def get_success_url(self):
        if 'save_continue' in self.request.POST:
            return self.request.path
        else:
            return self.get_finished_url()

    def get_finished_url(self):
        return self.get_list_url()
