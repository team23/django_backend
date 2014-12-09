from django.forms.models import _get_foreign_key

from .renderable import Renderable
from .form_tabs import BaseFormElement


class InlineRelatedObject(Renderable):
    """
    Represents one item in the list of related items. That contains a preview
    for the object plus the edit/delete buttons.
    """

    template_name = 'django_backend/inline_related/_inline_related_object.html'


class InlineRelated(BaseFormElement):
    template_name = 'django_backend/inline_related/_one_to_many.html'

    def __init__(self, parent_backend, backend, label=None, *args, **kwargs):
        self.parent_backend = parent_backend
        self.backend = backend
        self.label = label
        self.fk = self.get_related_field()
        super(InlineRelated, self).__init__(*args, **kwargs)

    def get_context_data(self, context, **kwargs):
        instance = self.resolve_instance(context)
        kwargs.update({
            'backend': self.backend,
            'model': self.backend.model,
            'opts': self.backend.model._meta,
            'object': instance,
            'object_list': self.get_queryset(instance),
            'related_field': self.fk,
        })
        return kwargs

    def get_queryset(self, related_instance, queryset=None):
        if queryset is None:
            queryset = self.backend.model._default_manager
        if related_instance.pk is not None:
            queryset = queryset.filter(**{self.fk.name: related_instance})
        else:
            queryset = queryset.none()
        return queryset

    def get_related_field(self):
        return _get_foreign_key(
            parent_model=self.parent_backend.model,
            model=self.backend.model)

    def resolve_instance(self, context):
        """
        Return instance from context.
        """
        if 'form' not in context:
            # we need the form to exists
            # create new empty instance
            return self.fk.rel.to()
        try:
            return context['form'].instance
        except KeyError:
            # create new empty instance
            return self.fk.rel.to()

    def resolve_label(self, context):
        return self.label or self.backend.model._meta.verbose_name_plural

    def resolve_required(self, context):
        return False
