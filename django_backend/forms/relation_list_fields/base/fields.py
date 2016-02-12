from django_backend.forms import BaseBackendInlineFormSet
from django_backend.forms import InlineFormSetField


__all__ = ('BaseRelationListField',)


class BaseRelationListField(InlineFormSetField):
    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------

        ``related_models`` : list
            (optional) can be a list of models that you are able to add to this
            relation. It might be more than one (where the ForeignKey is
            pointing to) if you are using model inheritance (FK links to model
            A, model B inherits from model A, so you can link to model B as
            well).
        """
        self.related_models = kwargs.pop('related_models', None)
        self.order_field = kwargs.pop('order_field', None)

        kwargs.setdefault('formset', BaseBackendInlineFormSet)
        kwargs.setdefault('exclude', ())
        super(BaseRelationListField, self).__init__(*args, **kwargs)

        if self.related_models is None:
            self.related_models = self.get_related_models()
        self.widget.set_related_models(self.related_models)

    def get_related_models(self):
        # Needs to be implemented by subclasses.
        return []

    def get_kwargs(self, form, name):
        kwargs = super(BaseRelationListField, self).get_kwargs(form, name)
        kwargs.setdefault('order_field', self.order_field)
        return kwargs
