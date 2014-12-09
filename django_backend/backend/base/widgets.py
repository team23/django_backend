import floppyforms.__future__ as forms
from django.core.validators import EMPTY_VALUES


class SelectRelatedWidget(forms.TextInput):
    is_hidden = False
    type = 'hidden'
    template_name = None

    def __init__(self, *args, **kwargs):
        self.field = kwargs.pop('field')
        self.inline_backend = kwargs.pop('inline_backend')
        kwargs.setdefault('template_name', self.get_template_name())
        super(SelectRelatedWidget, self).__init__(*args, **kwargs)

    def get_template_name(self):
        opts = self.inline_backend.model._meta
        format_kwargs = {
            'app_label': opts.app_label,
            'object_name': opts.object_name.lower(),
        }
        return [
            'django_backend/{app_label}/{object_name}_select_related_widget.html'.format(**format_kwargs),
            'django_backend/forms/select_related.html',
        ]

    def get_preview(self, object):
        return self.inline_backend.get_preview(object)

    def get_context(self, name, value, attrs=None):
        context = super(SelectRelatedWidget, self).get_context(name, value, attrs=attrs)
        queryset = self.field.queryset
        context['inline_backend'] = self.inline_backend
        context['required'] = self.field.required
        if value not in EMPTY_VALUES:
            try:
                object = queryset.get(pk=value)
                context['preview'] = self.get_preview(object)
            except queryset.model.DoesNotExist:
                pass
        return context
