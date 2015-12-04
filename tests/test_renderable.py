from django.template import Context
from django.template import Template
from django.template import TemplateDoesNotExist
from django.test import TestCase

from django_backend import Renderable


class DoomedRenderable(Renderable):
    def render(self, context=None):
        raise Exception('Completely unexcepted exception.')


class RenderableErrorHandling(TestCase):
    def test_propagates_error(self):
        renderable = DoomedRenderable()
        with self.assertRaises(Exception):
            renderable.render()

    def test_non_existent_template_raises_error(self):
        renderable = Renderable(template_name='non_existent!')
        with self.assertRaises(TemplateDoesNotExist):
            renderable.render()

    def test_render_tag_does_not_swallow_error(self):
        renderable = Renderable(template_name='non_existent!')
        template = Template(
            '''
            {% load django_backend_tags %}
            {% render renderable %}
            ''')
        with self.assertRaises(TemplateDoesNotExist):
            template.render(Context({'renderable': renderable}))

    def test_render_tag_does_not_swallow_nested_error(self):
        render_object = Renderable(template_name='render_object.html')
        renderable = Renderable(template_name='non_existent!')
        template = Template(
            '''
            {% load django_backend_tags %}
            {% render render_object %}
            ''')
        with self.assertRaises(TemplateDoesNotExist):
            template.render(Context({
                'render_object': render_object,
                'object': renderable
            }))
