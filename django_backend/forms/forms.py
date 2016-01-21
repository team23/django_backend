from django.db import models
from django.forms.models import BaseInlineFormSet as _BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from django_superform import SuperModelForm
from django_superform.forms import SuperModelFormMetaclass
from floppyforms import fields
from floppyforms.__future__.models import formfield_callback as floppyforms_formfield_callback
from floppyforms.__future__.models import ModelFormMetaclass as FloppyformsModelFormMetaclass
import floppyforms.__future__ as forms

from .selectrelated import SelectRelatedField


__all__ = (
    'FORMFIELD_OVERRIDES', 'FORMFIELD_OVERRIDE_DEFAULTS',
    'add_formfield_override', 'formfield_callback', 'BackendFormMetaclass',
    'BaseBackendForm', 'CopyOnTranslateInlineFormSetMixin',
    'BaseBackendInlineFormSet')


FORMFIELD_OVERRIDES = {
    models.ForeignKey: {'form_class': SelectRelatedField},
}

FORMFIELD_OVERRIDE_DEFAULTS = {'choices_form_class': fields.TypedChoiceField}


def add_formfield_override(db_field, overrides):
    """
    Allow external apps to add new overrides so that custom db fields can use
    custom form fields in the backend.
    """
    current_overrides = FORMFIELD_OVERRIDES.setdefault(db_field, {})
    current_overrides.update(overrides)


def formfield_callback(db_field, **kwargs):
    defaults = FORMFIELD_OVERRIDE_DEFAULTS.copy()
    if hasattr(db_field, 'rel') and hasattr(db_field.rel, 'to'):
        lookup = (db_field.__class__, db_field.rel.to)
        if lookup in FORMFIELD_OVERRIDES:
            defaults.update(FORMFIELD_OVERRIDES[lookup])
            defaults.update(kwargs)
            return db_field.formfield(**defaults)
    if db_field.__class__ in FORMFIELD_OVERRIDES:
        defaults.update(FORMFIELD_OVERRIDES[db_field.__class__])
        defaults.update(kwargs)
        return db_field.formfield(**defaults)
    return floppyforms_formfield_callback(db_field, **kwargs)


class BackendFormMetaclass(SuperModelFormMetaclass, FloppyformsModelFormMetaclass):
    def __new__(mcs, name, bases, attrs):
        if 'formfield_callback' not in attrs:
            attrs['formfield_callback'] = formfield_callback
        return super(BackendFormMetaclass, mcs).__new__(
            mcs, name, bases, attrs)


class BaseBackendForm(SuperModelForm, forms.ModelForm):
    '''
    This is the base form that should be used by all backends. It
    handles the language of objects as expected.
    '''

    __metaclass__ = BackendFormMetaclass

    class Meta:
        exclude = ()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BaseBackendForm, self).__init__(*args, **kwargs)
        self.bind_widgets()

    def bind_widgets(self):
        for field in self.fields.values():
            if hasattr(field.widget, 'bind_to_form'):
                field.widget.bind_to_form(self)

    @property
    def extra_fields(self):
        return [self[name] for name in self.composite_fields]


class CopyOnTranslateInlineFormSetMixin(object):
    '''
    Takes care of the logic to replace the relations in the inline objects if
    the formset's instance is different to the objects foreign key.

    This is the case if the form is going to be translated.
    '''

    def clone_object(self, obj, commit):
        related_object = self.instance
        if obj.pk is not None:
            return obj.clone(attrs={
                self.fk.name: related_object,
            }, commit=commit)
        else:
            setattr(obj, self.fk.name, related_object)
            if commit:
                obj.save()
            return obj

    def related_has_changed(self, obj):
        return getattr(obj, self.fk.get_attname()) != self.instance.pk

    # This is a (nearly) exact copy from the base class. The only difference is
    # that we did put in the delete_object hook.
    def save_existing_objects(self, commit=True):
        self.changed_objects = []
        self.deleted_objects = []
        if not self.initial_forms:
            return []

        saved_instances = []
        forms_to_delete = self.deleted_forms
        for form in self.initial_forms:
            pk_name = self._pk_field.name
            raw_pk_value = form._raw_value(pk_name)

            # clean() for different types of PK fields can sometimes return
            # the model instance, and sometimes the PK. Handle either.
            pk_value = form.fields[pk_name].clean(raw_pk_value)
            pk_value = getattr(pk_value, 'pk', pk_value)

            obj = self._existing_object(pk_value)
            if form in forms_to_delete:
                self.deleted_objects.append(obj)
                # THIS IS THE REASON WHY WE DUPLICATE THIS METHOD FROM THE BASE
                # CLASS.
                # We need a hook for deleting objects.
                self.delete_object(form, obj)
                continue
            if form.has_changed() or self.related_has_changed(obj):
                self.changed_objects.append((obj, form.changed_data))
                saved_instances.append(self.save_existing(form, obj, commit=commit))
                if not commit:
                    self.saved_forms.append(form)
        return saved_instances

    def delete_object(self, form, obj):
        # Only delete when we have not cloned.
        if not self.related_has_changed(obj):
            obj.delete()

    def save_object(self, form, commit=True, form_save_kwargs=None):
        form_save_kwargs = form_save_kwargs or {}
        obj = form.save(commit=False, **form_save_kwargs)
        if self.related_has_changed(obj):
            return self.clone_object(obj, commit=commit)
        if commit:
            obj.save()
        if commit and hasattr(form, 'save_m2m'):
            form.save_m2m()
        return obj

    def save_existing(self, form, instance, commit=True):
        return self.save_object(form, commit=commit)

    def save_new(self, form, commit=True):
        return self.save_object(form, commit=commit)


class BaseBackendInlineFormSet(CopyOnTranslateInlineFormSetMixin, _BaseInlineFormSet):
    '''
    Should be used for all inline formsets in the backend.
    It takes care of copying the related objects on a translate.
    '''

    def __init__(self, *args, **kwargs):
        self.order_field = kwargs.pop('order_field', None)
        self.min_forms = kwargs.pop('min_forms', None)
        super(BaseBackendInlineFormSet, self).__init__(*args, **kwargs)

        # Order the inline queryset if possible.
        if self.order_field is None:
            self.order_field = getattr(self.model, 'order_field', None)
        if self.order_field:
            self.queryset = self.queryset.order_by(self.order_field)

    def add_fields(self, form, index):
        super(BaseBackendInlineFormSet, self).add_fields(form, index)

        if self.order_field and self.order_field in form.fields:
            form.fields[self.order_field].widget = forms.HiddenInput()
        if self.can_delete:
            form.fields['DELETE'].widget = forms.HiddenInput()

    def filled_form_count(self):
        '''
        Return the number of forms that the user has actually filled out.
        '''
        deleted_forms = self.deleted_forms
        return len([
            form
            for form in self.forms
            if getattr(form, 'cleaned_data', None) and form not in deleted_forms])

    def full_clean(self):
        super(BaseBackendInlineFormSet, self).full_clean()
        if self.min_forms:
            if self.is_bound:
                if self.filled_form_count() < self.min_forms:
                    self._non_form_errors.append(_('Please add at least %(min_forms)s item.') % {
                        'min_forms': self.min_forms,
                    })


# class TranslatableForm(BaseBackendForm):
#     def __init__(self, *args, **kwargs):
#         self.origin = kwargs.pop('origin', None)
#
#         instance = kwargs.pop('instance', None)
#         create = not (instance and instance.pk)
#
#         if self.origin is not None and create:
#             instance = self.origin.clone(commit=False)
#
#         kwargs['instance'] = instance
#         super(BaseBackendForm, self).__init__(*args, **kwargs)
#
#     def set_language(self):
#         self.instance.language = language.active
#         if self.origin is not None:
#             self.instance.translation_set = self.origin.translation_set
#
#     def save(self, *args, **kwargs):
#         create = self.instance.pk is None
#         if create:
#             self.set_language()
#         return super(BaseBackendForm, self).save(*args, **kwargs)
#
#
# class VersionableForm(BaseBackendForm):
#     '''
#     A base form for models that inherit from VersionableMixin. They do always
#     come together with a RevisionForm and therefore need a bit extra handling
#     (e.g. they want to ignore the clonable stuff).
#     '''
#
#     class Meta:
#         exclude = (
#             'translation_set',
#             'language',
#         )
#
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request')
#         self.origin = kwargs.pop('origin', None)
#
#         # Do not process origin here and try to clone it. That will happen in
#         # RevisionForm for the revisioned model.
#
#         forms.ModelForm.__init__(self, *args, **kwargs)
#
#
# class RevisionForm(BaseBackendForm):
#     '''
#     And a base form for all revisionable models (mostly pages).
#     Should be used on page backends.
#     '''
#
#     class Meta:
#         exclude = (
#             'revision_parent',
#             'revision_author',
#             'is_working_copy',
#             'working_copy_expires',
#         )
#
#     def __init__(self, *args, **kwargs):
#         self.save_working_copy = kwargs.pop('save_working_copy', None)
#         self.save_branch = kwargs.pop('save_branch', None)
#
#         super(RevisionForm, self).__init__(*args, **kwargs)
#
#         # Remove the field that points to the base object.
#         parent_field = self._meta.model._versionable_foreign_key
#         del self.fields[parent_field]
#
#     def set_language(self, origin):
#         # Translations are handled in VersionableForm.
#         pass
#
#     def save(self, *args, **kwargs):
#         create = self.instance.pk is None
#
#         # If a new component item is created, we need to save to a branch.
#         # Saving to a working copy wouldn't make sense.
#         assert not create or self.save_branch
#
#         if self.save_branch:
#             self.instance.is_working_copy = False
#             self.instance.working_copy_expires = None
#         # if self.save_working_copy then we don't need to do anything since
#         # django's default machinery is what we want.
#         if self.save_working_copy:
#             pass
#
#         if create:
#             base_object = kwargs.pop('base_object')
#             setattr(self.instance, self.instance._versionable_foreign_key, base_object)
#
#         self.instance.revision_author = self.request.user
#
#         result = super(RevisionForm, self).save(*args, **kwargs)
#
#         # make sure m2m relations are cloned, too
#         if kwargs.get('commit', True) and hasattr(result, 'clone_m2m'):
#             result.clone_m2m()
#
#         # We cannot account for the commit argument here, since set_branch
#         # needs a primary key to be available. And if this object is about to
#         # be created and commit=False was passed... we don't have a pk here. So
#         # in this case it will blow up loudly.
#         assert self.instance.pk is not None
#         if self.save_branch:
#             self.instance.set_branch(slug=self.save_branch)
#
#         return result
