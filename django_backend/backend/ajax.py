import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.template import Context
from django.template import RequestContext
from django.template.loader import render_to_string, select_template
from django.utils.encoding import force_unicode

from ..compat import context_flatten
from ..compat import get_template_name


class JsonResponseMixin(object):
    status = 'ok'
    json_encoder_class = DjangoJSONEncoder

    def get_json(self, **kwargs):
        json_data = {
            'status': self.status,
        }
        json_data.update(kwargs)
        return json_data

    def render_json_response(self, json_data, **response_kwargs):
        json_serialized = json.dumps(
            json_data,
            cls=self.json_encoder_class)
        json_serialized = json_serialized.encode('utf-8')
        return HttpResponse(json_serialized,
                            content_type='application/json; charset=utf-8',
                            **response_kwargs)


class DialogResponseMixin(JsonResponseMixin):
    '''
    Use this mixin to provide valid responses for calls from the AjaxDialog
    classes in the client.

    Subclasses need to have a ``get_template_names`` method that returns the
    template names that should be rendered inside the
    ``page_wrapper_template_name``.

    The mixin returns JSON if ``request.is_ajax() == True``. The return value
    of the ``get_json()`` method is therefore serialized to JSON.
    '''

    title = None

    page_wrapper_template_name = 'django_backend/page_wrapper.html'

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        kwargs.setdefault('title', self.get_title())
        kwargs['is_dialog'] = self.is_dialog()
        return super(DialogResponseMixin, self).get_context_data(**kwargs)

    def get_page_wrapper_template_names(self):
        '''
        Returns the wrapper template name that takes the real template names to
        be rendered inside.
        '''
        return [self.page_wrapper_template_name]

    def is_dialog(self):
        return self.request.is_ajax()

    def get_json(self, **kwargs):
        json_data = super(DialogResponseMixin, self).get_json(**kwargs)
        title = self.get_title()
        if title:
            json_data['title'] = force_unicode(title)
        return json_data

    def render_to_response(self, context, **response_kwargs):
        if self.is_dialog():
            context = RequestContext(self.request, context)
            context.update(self.get_context_data())
            json_data = self.get_json()
            json_data['html'] = render_to_string(
                self.get_template_names(), context)
            return self.render_json_response(json_data, **response_kwargs)
        else:
            return self.render_html_response(context, **response_kwargs)

    def render_html_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        template = select_template(self.get_template_names())
        context['template_name'] = get_template_name(template)
        return self.response_class(
            request=self.request,
            template=self.get_page_wrapper_template_names(),
            context=context,
            **response_kwargs)
