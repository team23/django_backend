from django.template.response import TemplateResponse
from django.test import TestCase
from django.views.generic import TemplateView
from mock import Mock
import json

from django_backend.backend.ajax import DialogResponseMixin


class SimpleTemplateView(DialogResponseMixin, TemplateView):
    template_name = 'static_content.html'


class DialogResponseMixinTest(TestCase):
    def setUp(self):
        self.request = Mock()
        self.request.is_ajax.return_value = False
        self.ajax_request = Mock()
        self.ajax_request.is_ajax.return_value = True

    def test_normal_request(self):
        view = SimpleTemplateView(request=self.request)

        response = view.render_to_response({})
        self.assertTrue(isinstance(response, TemplateResponse))
        self.assertEqual(response.template_name,
                         ['django_backend/page_wrapper.html'])
        self.assertEqual(response.context_data['template_name'],
                         'static_content.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_ajax_request(self):
        view = SimpleTemplateView(request=self.ajax_request)

        response = view.render_to_response({})
        self.assertTrue(not isinstance(response, TemplateResponse))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')
        data = json.loads(response.content)
        # We strip to remove trailing newline.
        self.assertEqual(data['html'].strip(), 'static content')
        self.assertEqual(data['status'], 'ok')
