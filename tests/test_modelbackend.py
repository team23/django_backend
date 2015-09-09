from django.test import TestCase

from django_backend.backend.base.backends import ModelBackend
from django_backend.sitebackend import SiteBackend

from .models import OneFieldModel


class ModelBackendTest(TestCase):
    def setUp(self):
        self.site = SiteBackend(id='test')

    def get_basic_backend(self, **kwargs):
        defaults = {
            'id': 'onefieldmodel',
            'model': OneFieldModel,
        }
        defaults.update(**kwargs)
        return self.site.register(ModelBackend, **defaults)

    def test_registration(self):
        self.site.register(
            ModelBackend,
            id='onefieldmodel',
            model=OneFieldModel)

    def test_get_form_class(self):
        backend = self.get_basic_backend()
        form_class = backend.get_form_class()

        self.assertEqual(form_class.Meta.model, OneFieldModel)
        self.assertEqual(form_class.base_fields.keys(), ['name'])
