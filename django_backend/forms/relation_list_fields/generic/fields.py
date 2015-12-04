import floppyforms.__future__ as forms

from ..base import BaseRelationListField
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


class GenericRelationListField(BaseRelationListField):
    widget = GenericRelationListWidget

    def __init__(self, *args, **kwargs):
        assert 'related_models' in kwargs, (
            'related_models argument is required')

        model = kwargs['model']
        kwargs.setdefault('form', get_default_form(
            model,
            kwargs.get('order_field', None)))
        super(GenericRelationListField, self).__init__(*args, **kwargs)
        self.widget.set_content_type_field_name('content_type')
