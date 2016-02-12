import floppyforms.__future__ as forms

from ..base import BaseRelationListField
from .widgets import M2MListWidget


__all__ = ('M2MListField',)


def get_default_form(model, foreignkey_name, order_field):
    form_fields = (foreignkey_name,)

    if order_field:
        form_fields = (order_field,) + form_fields

    class M2MListForm(forms.ModelForm):
        class Meta:
            fields = form_fields

    return M2MListForm


class M2MListField(BaseRelationListField):
    widget = M2MListWidget

    def __init__(self, *args, **kwargs):
        self.foreignkey_name = kwargs.pop('foreignkey_name')

        model = kwargs['model']
        kwargs.setdefault('form', get_default_form(
            model,
            self.foreignkey_name,
            kwargs.get('order_field', None)))
        super(M2MListField, self).__init__(*args, **kwargs)
        self.widget.set_object_id_field_name(self.foreignkey_name)

    def get_related_models(self):
        fk = self.model._meta.get_field(self.foreignkey_name)
        return [fk.rel.to]
