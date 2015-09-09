from django.contrib.auth.models import User
from django.test import TestCase
from django_dynamic_fixture import get

from django_backend.backend.base.backends import ModelBackend
from django_backend.sitebackend import SiteBackend

from .models import ForeignKeyModel
from .models import OneFieldModel


class ModelBackendRegistrationTest(TestCase):
    def test_registration(self):
        site = SiteBackend(id='test')
        site.register(
            ModelBackend,
            id='onefieldmodel',
            model=OneFieldModel)


class ModelBackendTest(TestCase):
    def setUp(self):
        self.site = SiteBackend(id='test')
        self.onefieldmodel = self.site.register(
            ModelBackend,
            id='onefieldmodel',
            model=OneFieldModel)
        self.fkmodel = self.site.register(
            ModelBackend,
            id='fkmodel',
            model=ForeignKeyModel)

    def get_basic_backend(self, **kwargs):
        defaults = {
            'id': 'onefieldmodel',
            'model': OneFieldModel,
        }
        defaults.update(**kwargs)
        return self.site.register(ModelBackend, **defaults)

    def test_get_form_class(self):
        form_class = self.onefieldmodel.get_form_class()

        self.assertEqual(form_class.Meta.model, OneFieldModel)
        self.assertEqual(form_class.base_fields.keys(), ['chars'])

    def test_get_to_be_deleted_objects(self):
        user = get(User)

        fk_instance = get(ForeignKeyModel)
        onefield_instance = fk_instance.fk

        results = self.onefieldmodel.get_to_be_deleted_objects(
            objects=[onefield_instance], user=user)

        to_delete, perms_needed, protected = results

        self.assertEqual(len(to_delete), 2)
        self.assertEqual(to_delete[0]['object'], onefield_instance)
        self.assertEqual(to_delete[0]['backend'], self.onefieldmodel)

        nested = to_delete[1]
        self.assertEqual(len(nested), 1)
        self.assertEqual(nested[0]['object'], fk_instance)
        self.assertEqual(nested[0]['backend'], self.fkmodel)
