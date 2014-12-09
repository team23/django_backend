from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _


class BackendPermissionViewMixin(object):
    '''
    Base mixin for views that are checking permissions.
    '''

    def get_required_permissions(self):
        return ['django_backend.access_backend']

    def get_required_object_permissions(self):
        return []

    def has_perm(self, perm, obj=None):
        '''
        Checks if the request's user has the given permission. The permission
        will actually be checked by the backend. You can give a shortcut like::

            self.has_perm('change')

        Instead of including the model name::

            self.has_perm('change_page')
        '''
        return self.backend.has_perm(self.request.user, perm, obj)

    def check_permission(self):
        '''
        Override this if you need to implement a sophisticated hook that is not
        just done with ``user.has_perm`` checks.

        Ideally you don't need this and everything is implemented by using
        callable perms.

        This will only be called if the other permission checks were successfull.
        '''
        return True

    def _check_permissions(self):
        # Do not allow access for any non logged in user.
        if not self.request.user.is_authenticated():
            return self.redirect_to_login()

        # Do not allow access for any non-staff user.
        if not self.request.user.has_perm('django_backend.access_backend'):
            raise PermissionDenied

        # First check the permissions given by the
        # ``get_required_permissions`` method.
        for permission in self.get_required_permissions():
            if not self.has_perm(permission):
                raise PermissionDenied

        # If there is a object set for this view, we need to check if we are
        # allowed to access it.
        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if obj is not None:
                for permission in self.get_required_object_permissions():
                    if not self.has_perm(permission, obj):
                        raise PermissionDenied

        # Now this is a hook we can implement more sophisticated checks.
        if not self.check_permission():
            raise PermissionDenied

    def pre_dispatch(self, request, *args, **kwargs):
        response = self._check_permissions()
        if response:
            return response
        return super(BackendPermissionViewMixin, self).pre_dispatch(request, *args, **kwargs)

    def redirect_to_login(self):
        urlname = self.backend.base.urlnames.views['login'].name
        return HttpResponseRedirect('{0}?next={1}'.format(
            reverse(urlname),
            self.request.path))

    def get_permission_denied_redirect_url(self):
        urlname = self.backend.base.urlnames.views['index'].name
        return self.reverse(urlname)

    def handle_permission_denied(self, request, exception):
        '''
        Display an error message and redirect to a url defined by
        ``get_permission_denied_redirect_url``.
        '''
        # Only redirect the user to the backend index if the user can access
        # it.
        if self.request.user.has_perm('django_backend.access_backend'):
            message = unicode(exception)
            if not message:
                message = _("You don't have the required permissions.")
            messages.error(request, _('Sorry, you cannot access this page. %(message)s') % {
                'message': message,
            })
            return HttpResponseRedirect(self.get_permission_denied_redirect_url())
        # Re-raise to return a 403 response.
        raise exception
