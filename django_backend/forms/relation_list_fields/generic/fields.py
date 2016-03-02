import floppyforms.__future__ as forms
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from ..base import BaseRelationListField
from .widgets import GenericRelationListWidget


__all__ = ('GenericRelationListField',)


def get_default_form(model, ct_field, fk_field, order_field, related_models):
    form_fields = (ct_field, fk_field)
    if order_field:
        form_fields = (order_field,) + form_fields

    class GenericRelationListForm(forms.ModelForm):
        class Meta:
            fields = form_fields

        def clean(self):
            cleaned_data = super(GenericRelationListForm, self).clean()
            content_type = cleaned_data.get(ct_field)
            if content_type:
                if content_type.model_class() not in related_models:
                    self.add_error(field=ct_field, error=_(
                        'The selected type {type} is not allowed here. '
                        'Choose one of the following: {allowed}'.format(
                            type=content_type,
                            allowed=', '.join(
                                force_text(model._meta.verbose_name)
                                for model in related_models))
                    ))
            return cleaned_data

    return GenericRelationListForm


class GenericRelationListField(BaseRelationListField):
    widget = GenericRelationListWidget

    def __init__(self, *args, **kwargs):
        assert 'related_models' in kwargs, (
            'related_models argument is required')

        self.generic_fk_name = kwargs.pop('generic_fk_name', None)

        model = kwargs['model']
        generic_fk = self.get_generic_foreign_key(model)
        kwargs.setdefault('form', get_default_form(
            model=model,
            order_field=kwargs.get('order_field', None),
            fk_field=generic_fk.fk_field,
            ct_field=generic_fk.ct_field,
            related_models=kwargs['related_models']))
        super(GenericRelationListField, self).__init__(*args, **kwargs)

        self.determine_generic_relation_fields(model)

    def get_generic_foreign_key(self, model):
        if self.generic_fk_name is not None:
            return model._meta.get_field(self.generic_fk_name)
        generic_fks = [
            field
            for field in model._meta.get_fields()
            if isinstance(field, GenericForeignKey)]
        assert len(generic_fks) == 1, (
            'Given model {model} requires exactly one GenericForeignKey.')
        return generic_fks[0]

    def determine_generic_relation_fields(self, model):
        generic_fk = self.get_generic_foreign_key(model)
        self.widget.set_object_id_field_name(generic_fk.fk_field)
        self.widget.set_content_type_field_name(generic_fk.ct_field)
