import floppyforms.__future__ as floppyforms
from django.test import TestCase

from django_backend.forms import BaseBackendForm

from .models import OneFieldModel


class OneFieldForm(BaseBackendForm):
    class Meta:
        model = OneFieldModel
        exclude = ()


class BaseBackendFormTests(TestCase):
    def test_has_superform_metaclass(self):
        from django_superform.forms import SuperModelFormMetaclass

        self.assertTrue(
            issubclass(BaseBackendForm.__metaclass__, SuperModelFormMetaclass))

    def test_has_floppyforms_metaclass(self):
        from floppyforms.__future__.models import ModelFormMetaclass

        self.assertTrue(
            issubclass(BaseBackendForm.__metaclass__, ModelFormMetaclass))

    def test_model_field_is_using_floppyforms_widget(self):
        form = OneFieldForm()
        self.assertTrue(
            isinstance(form.fields['chars'].widget, floppyforms.TextInput))
