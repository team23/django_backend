import floppyforms.__future__ as forms
from floppyforms.widgets import Input
from django.core.validators import EMPTY_VALUES


__all__ = (
    'SelectRelatedField', 'SelectRelatedWidget', 'ManageRelatedField',
    'ManageRelatedWidget')


class BindWidgetMixin(object):
    bound_field = None
    bound_form = None

    def bind_to_field(self, field):
        assert self.bound_field is None
        self.bound_field = field

    def bind_to_form(self, form):
        assert self.bound_form is None
        self.bound_form = form


class BaseRelatedWidgetMixin(BindWidgetMixin):
    is_hidden = False
    input_type = 'hidden'
    template_name = None

    def __init__(self, *args, **kwargs):
        self.inline_backend = kwargs.pop('inline_backend', None)
        super(BaseRelatedWidgetMixin, self).__init__(*args, **kwargs)

    def get_inline_backend(self):
        if self.inline_backend is not None:
            return self.inline_backend
        return self.bound_field.get_inline_backend(
            parent_backend=self.get_parent_backend())

    def get_parent_backend(self):
        """
        That looks like a hack but gives a great deal of flexibility.

        We try to retrieve the current backend in use (in which this widget is
        rendered) from the template context. We then use this backend as a
        starting point to look for a specific inline backend.

        That way we prefer the nested inline backend before the global ones.
        That makes it possible to overwrite the backends used for a
        SelectRelatedField without overwriting the field itself.
        """
        from django_backend.backend import BaseBackend

        if hasattr(self, 'context_instance'):
            if 'backend' in self.context_instance:
                backend = self.context_instance['backend']
                if isinstance(backend, BaseBackend):
                    return backend
        return None

    def render(self, *args, **kwargs):
        kwargs.setdefault('template_name', self.get_template_name())
        return super(BaseRelatedWidgetMixin, self).render(*args, **kwargs)


class SelectRelatedWidget(BaseRelatedWidgetMixin, forms.TextInput):
    is_hidden = False
    type = 'hidden'
    template_name = None

    def get_template_name(self):
        if self.template_name is not None:
            return self.template_name
        opts = self.get_inline_backend().model._meta
        format_kwargs = {
            'app_label': opts.app_label,
            'object_name': opts.object_name.lower(),
        }
        return [
            'django_backend/{app_label}/{object_name}_select_related_widget.html'.format(**format_kwargs),
            'django_backend/forms/select_related.html',
        ]

    def get_preview(self, object):
        return self.get_inline_backend().get_preview(object)

    def get_context(self, name, value, attrs=None):
        context = super(SelectRelatedWidget, self).get_context(name, value, attrs=attrs)
        queryset = self.bound_field.queryset
        context['inline_backend'] = self.get_inline_backend()
        context['required'] = self.bound_field.required
        if value not in EMPTY_VALUES:
            try:
                object = queryset.get(pk=value)
                context['preview'] = self.get_preview(object)
            except queryset.model.DoesNotExist:
                pass
        return context


class ManageRelatedWidget(BaseRelatedWidgetMixin, Input):
    def get_template_name(self):
        if self.template_name is not None:
            return self.template_name
        opts = self.get_inline_backend().model._meta
        format_kwargs = {
            'app_label': opts.app_label,
            'object_name': opts.object_name.lower(),
        }
        return [
            (
                'django_backend/{app_label}/'
                '{object_name}_manage_related_widget.html'.format(
                    **format_kwargs)
            ),
            'django_backend/forms/manage_related.html',
        ]

    def get_preview(self, object):
        return self.get_inline_backend().get_preview(object)

    def get_instance(self):
        if self.bound_form:
            return getattr(self.bound_form, 'instance', None)
        else:
            return None

    def get_instance_pk(self):
        return getattr(self.get_instance(), 'pk', None)

    def get_context(self, name, value, attrs=None):
        context = super(ManageRelatedWidget, self).get_context(name, value, attrs=attrs)
        instance_pk = self.get_instance_pk()
        inline_backend = self.get_inline_backend()
        context['parent_exists'] = instance_pk is not None
        context['parent_pk'] = self.get_instance_pk()
        context['inline_backend'] = inline_backend
        context['required'] = self.bound_field.required
        context['related_field_name'] = self.bound_field.related_field_name
        return context


class BaseRelatedFieldMixin(object):
    def __init__(self, *args, **kwargs):
        widget = self.inline_widget_class()
        kwargs.setdefault('widget', widget)
        super(BaseRelatedFieldMixin, self).__init__(*args, **kwargs)
        if hasattr(self.widget, 'bind_to_field'):
            self.widget.bind_to_field(self)


class SelectRelatedField(BaseRelatedFieldMixin, forms.ModelChoiceField):
    inline_widget_class = SelectRelatedWidget

    def __init__(self, *args, **kwargs):
        self.inline_backend = kwargs.pop('inline_backend', None)
        super(SelectRelatedField, self).__init__(*args, **kwargs)

    def get_model(self):
        return self.queryset.model

    def get_inline_backend(self, parent_backend=None):
        if self.inline_backend is not None:
            return self.inline_backend

        if parent_backend is not None:
            return parent_backend.find(
                model=self.get_model(),
                registry='inline')

        from django_backend import site
        return site.find(model=self.get_model(), registry='inline')


class ManageRelatedField(BaseRelatedFieldMixin, forms.CharField):
    """
    Manage multiple related objects (associated with a ForeignKey) via a inline
    backend. The widget will only display the related objects, but changing
    them will happen in a modal showing an inline backend.

    The relation will be saved once the modal is saved, not on save of the form
    where this field is used. This implies that no relation can be created
    before the object this field operates on was saved the first time.

    You must give the field a backend instance for the ``inline_backend``
    argument and the name of foreign key to the parent model as
    ``related_field_name``.

    The given backend should have a filter form in place that can filter on the
    ``related_field_name``. Otherwise the backend will likely also show objects
    that are not related.
    """
    inline_widget_class = ManageRelatedWidget

    def __init__(self, *args, **kwargs):
        self.inline_backend = kwargs.pop('inline_backend')
        self.related_field_name = kwargs.pop('related_field_name')
        # There is no real data that could be validated associated with this
        # field. So we cannot require it.
        kwargs['required'] = False
        super(ManageRelatedField, self).__init__(*args, **kwargs)

    def get_model(self):
        return self.backend.model

    def get_inline_backend(self, parent_backend=None):
        return self.inline_backend
