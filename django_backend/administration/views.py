# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from ..backend.views import BackendViewMixin
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
import floppyforms.__future__ as forms


class AdministrationView(BackendViewMixin, TemplateView):
    template_name = 'django_backend/administration/index.html'

    def get_context_data(self, **kwargs):
        # log_entries = LogEntry.objects.visible_for_user(self.request.user)
        # kwargs['recent_changes'] = log_entries
        # kwargs['my_recent_changes'] = log_entries.filter(user=self.request.user)
        return super(AdministrationView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        if self.kwargs.get(self.language_url_kwarg) is None:
            return HttpResponseRedirect(
                reverse('django_backend:index',
                    kwargs={
                        'site': self.site_id,
                        'language': self.language_id,
                    }))
        return super(AdministrationView, self).get(request, *args, **kwargs)



class DjangoBackendPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old password"), widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password (repeat)"), widget=forms.PasswordInput)


class PasswordChangeView(BackendViewMixin, TemplateView):
    template_name = 'django_backend/administration/password_change.html'

    def get_context_data(self, **kwargs):
        return super(PasswordChangeView, self).get_context_data(**kwargs)

    def handle(self, request, *args, **kwargs):
        redirect_to = reverse('django_backend:inline-administration-index',
                              kwargs={
                                  'site': self.site_id,
                                  'language': self.language_id,
                              })
        response = auth_views.password_change(
            request,
            template_name=self.get_template_names(),
            password_change_form=DjangoBackendPasswordChangeForm,
            post_change_redirect=redirect_to,
            extra_context=self.get_context_data(**kwargs),
        )
        if response.get('Location') == redirect_to:
            messages.success(request, _('Your password was successfully changed.'))
        return response

    get = post = handle
