from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


class SetAuthorOnObjectPrepareMixin(object):
    def prepare_object(self, origin):
        object = super(SetAuthorOnObjectPrepareMixin, self).prepare_object(origin)
        object.author = self.request.user
        return object


class SaveInlineDoneMixin(object):
    '''
    This mixin takes care that the correct JSON response is provided for AJAX
    save-object calls, including the rendered inline so that it can be shown
    in the regions of a content provider.
    '''

    def form_valid(self, *args, **kwargs):
        response = super(SaveInlineDoneMixin, self).form_valid(*args, **kwargs)
        if self.is_dialog() and isinstance(response, HttpResponseRedirect):
            json_data = self.get_success_json()
            return self.render_json_response(json_data)
        return response

    def dismiss(self, *args, **kwargs):
        response = super(SaveInlineDoneMixin, self).dismiss(*args, **kwargs)
        if self.is_dialog() and isinstance(response, HttpResponseRedirect):
            json_data = self.get_dismiss_json()
            return self.render_json_response(json_data)
        return response

    def get_success_json(self):
        return {
            'status': 'ok',
            'action': 'select',
            'object_id': self.object.pk,
            'content_type_id': ContentType.objects.get_for_model(
                self.object).pk,
            'urls': {
                'update': self.get_update_url(self.object),
            },
            'preview': self.get_preview(self.object),
            'inline_related': self.get_inline_related_object_preview(self.object),
        }

    def get_dismiss_json(self):
        return {
            'status': 'ok',
            'action': 'dismiss',
        }
