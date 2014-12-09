from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DeleteView

from .edit import BackendDismissViewMixin
from .mixins import SaveInlineDoneMixin


class BackendDeleteView(SaveInlineDoneMixin, BackendDismissViewMixin, DeleteView):
    template_type = 'delete'

    def get_required_object_permissions(self):
        return super(BackendDeleteView, self).get_required_object_permissions() + ['delete']

    def get_object(self, *args, **kwargs):
        obj = super(BackendDeleteView, self).get_object(*args, **kwargs)
        to_be_deleted_info = self.backend.get_to_be_deleted_objects(
            [obj], self.request.user)
        self.objects_to_delete = to_be_deleted_info[0]
        self.objects_perms_needed = to_be_deleted_info[1]
        self.objects_protected = to_be_deleted_info[2]
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BackendDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.handle_dismiss()
        if response:
            return response
        # This will call `self.delete`
        response = super(BackendDeleteView, self).post(request, *args, **kwargs)

        # Return json on success if it is a dialog.
        if self.is_dialog() and isinstance(response, HttpResponseRedirect):
            json_data = self.get_success_json()
            return self.render_json_response(json_data)
        return response

    def delete(self, request, *args, **kwargs):
        if self.objects_perms_needed:
            raise PermissionDenied(_(
                'You do not have enough permissions to delete the related '
                'objects.'))
        if self.objects_protected:
            raise PermissionDenied(_(
                'Some of the objects you want to delete are protected.'))
        self.backend.delete_object(self.get_object())
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def get_success_json(self):
        return {
            'status': 'ok',
            'action': 'delete',
        }

    def get_context_data(self, **kwargs):
        kwargs.setdefault('delete', True)
        kwargs.update({
            'to_delete': self.objects_to_delete,
            'perms_needed': self.objects_perms_needed,
            'protected': self.objects_protected,
        })
        return super(BackendDeleteView, self).get_context_data(**kwargs)

    def dismiss(self, request, *args, **kwargs):
        if self.is_dialog():
            json_data = self.get_dismiss_json()
            return self.render_json_response(json_data)
        return super(BackendDeleteView, self).dismiss(request, *args, **kwargs)

    def get_dismiss_url(self):
        return self.get_read_url(object=self.origin)

    def get_success_url(self):
        return self.get_list_url()
