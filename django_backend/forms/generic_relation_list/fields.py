import floppyforms.__future__ as forms

from django_backend.forms import BaseBackendInlineFormSet
from django_backend.forms import InlineFormSetField

from .widgets import GenericRelationListWidget


__all__ = ('GenericRelationListField',)


def get_default_form(model, order_field):
    form_fields = (
        'content_type',
        'object_id',
    )

    if order_field:
        form_fields = (order_field,) + form_fields

    class GenericRelationListForm(forms.ModelForm):
        class Meta:
            fields = form_fields

    return GenericRelationListForm


class GenericRelationListFormSet(BaseBackendInlineFormSet):
    def save(self, *args, **kwargs):
        return super(GenericRelationListFormSet, self).save(*args, **kwargs)


class GenericRelationListField(InlineFormSetField):
    widget = GenericRelationListWidget

    def __init__(self, *args, **kwargs):
        self.related_models = kwargs.pop('related_models')
        self.order_field = kwargs.pop('order_field', None)

        model = kwargs['model']
        kwargs.setdefault('form', get_default_form(model, self.order_field))
        kwargs.setdefault('formset', GenericRelationListFormSet)
        kwargs.setdefault('exclude', ())
        super(GenericRelationListField, self).__init__(*args, **kwargs)
        self.widget.set_related_models(self.related_models)

    def get_kwargs(self, form, name):
        kwargs = super(GenericRelationListField, self).get_kwargs(form, name)
        kwargs.setdefault('order_field', self.order_field)
        return kwargs
