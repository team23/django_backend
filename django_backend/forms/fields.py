from django_superform import FormSetWidget as _FormSetWidget
from django_superform import InlineFormSetField as _InlineFormSetField


__all__ = (
    'InlineFormSetWidget', 'CopyOnTranslateInlineFormSetFieldMixin',
    'InlineFormSetField',)


class InlineFormSetWidget(_FormSetWidget):
    template_name = 'django_backend/forms/formsetfield.html'


class CopyOnTranslateInlineFormSetFieldMixin(object):
    def get_kwargs(self, form, name):
        kwargs = super(CopyOnTranslateInlineFormSetFieldMixin, self).get_kwargs(form, name)
        if getattr(form, 'origin', None):
            if kwargs['instance'] is form.instance:
                kwargs['instance'] = form.origin
        return kwargs

    def save(self, form, name, formset, commit):
        if getattr(form, 'origin', None):
            # We need to update the formset's instance, otherwise we will
            # operate on the origin.
            formset.instance = form.instance
        return super(CopyOnTranslateInlineFormSetFieldMixin, self).save(
            form, name, formset, commit)


class InlineFormSetField(CopyOnTranslateInlineFormSetFieldMixin, _InlineFormSetField):
    widget = InlineFormSetWidget

    def __init__(self, *args, **kwargs):
        from .forms import formfield_callback, BaseBackendInlineFormSet

        # Override to use our own formfield_callback.
        kwargs.setdefault('formfield_callback', formfield_callback)
        # Use backend base infline form set. This contains some hooks we need.
        kwargs.setdefault('formset', BaseBackendInlineFormSet)
        kwargs.setdefault('extra', 0)
        kwargs.setdefault('exclude', ())
        super(InlineFormSetField, self).__init__(*args, **kwargs)
