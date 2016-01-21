from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import floppyforms.__future__ as forms

from ..backend.base.backends import ModelBackend
from ..forms import BaseBackendForm, FilterForm
from .. import site


class UserFilterForm(FilterForm):
    search = forms.CharField(label=_('Search'), required=False)

    def filter_queryset(self, queryset):
        queryset = super(UserFilterForm, self).filter_queryset(queryset)
        if self.cleaned_data.get('search'):
            queryset = queryset.filter(email__icontains=self.cleaned_data['search'])
        return queryset


class UserForm(BaseBackendForm):
    password_change = forms.CharField(label=_(u'Password'), widget=forms.PasswordInput(render_value=True), required=False)
    password_repeat = forms.CharField(label=_(u'Password (repeat)'), widget=forms.PasswordInput(render_value=True), required=False)

    class Meta:
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'groups',
            'last_login',
            'date_joined',
        )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['password_change'].required = True

    def clean_password_repeat(self):
        password = self.cleaned_data.get('password_change')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password != password_repeat:
            raise forms.ValidationError('The entered passwords to not match')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email__iexact=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('A user/client with this email address is already registered.')
        return email

    def save(self, *args, **kwargs):
        if self.cleaned_data.get('password_change'):
            self.instance.set_password(self.cleaned_data.get('password_change'))
        if not self.instance.pk:
            self.instance.is_staff = True
        return super(UserForm, self).save(*args, **kwargs)


class UserModelBackend(ModelBackend):
    form_class = UserForm
    filter_form_class = UserFilterForm

    def get_queryset(self):
        return super(UserModelBackend, self).get_queryset().filter(is_staff=True)

    def get_form_tab_definition(self):
        from ..backend.form_tabs import FormTab

        tabs = super(UserModelBackend, self).get_form_tab_definition()
        tabs.update({
            'permissions': FormTab(_('Permissions'), [
                {
                    'label': _('Is Active'),
                    'fields': ['is_active'],
                },
                {
                    'label': _('Groups'),
                    'fields': ['groups'],
                },
            ], position=200),
            'meta': FormTab(_('Meta'), [
                {
                    'label': _('Last Login'),
                    'fields': ['last_login'],
                },
                {
                    'label': _('Date Joined'),
                    'fields': ['date_joined'],
                },
            ], position=300),
        })
        return tabs


site.register(
    UserModelBackend,
    registry='admin',
    id='user',
    verbose_name=_('User'),
    verbose_name_plural=_('Users'),
    model=User)
