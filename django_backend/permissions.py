"""
There are three roles available to check for when using ``user.has_perm(...)``.

- ``auth.editor_permission``
- ``auth.chief_editor_permission``
  (includes all permissions that ``editor_permission`` has).
- ``auth.admin_permission``
  (includes all permissions that ``chief_editor_permission`` has).
"""

import re

from django.contrib.auth import get_permission_codename
import django_callable_perms
from django_callable_perms import register


class BaseModelBackendPermissions(object):
    """
    A class-based approach to registering model permissions with
    django_callable_perms.

    To add a new object-level permission create a subclass of this and add a
    method with the name ``check_<perm-name>_object_permission``. This will
    register this method as a check with django_callable_perms where the
    permission name is ``<perm-name>`` put into context of the model passed
    into the `__init__` method.

    For instance, if you pass the ``auth.User`` model and have a
    ``check_read_object_permission`` method, the actuall permission name will
    be ``auth.read_user``.

    You can also add non-object-level permission checks with the naming scheme
    for methods: ``check_<perm-name>_permission``.

    If you want to use a different permission name than what is used in the
    method's name, then attach the ``permission_name`` attribute of the method,
    for example::

        def check_read_permission(self, user, perm, obj):
            return True
        check_read_permission.permission_name = 'my_app.access_model'

    And here is how you would define your own checks::

        class SupportPermissions(BaseModelBackendPermissions):
            def check_read_permission(self, user, perm, obj):
                # We cannot allow generic read permissions, we need to know
                # about the object.
                return False

            def check_read_object_permission(self, user, perm, obj):
                # Give support user access based on how much we trust them and
                # how confidential the information is.
                if obj.is_confidential:
                    if user.is_trustworthy:
                        return True
                    else:
                        return False
                return True

    And then use the permissions::

        support_permissions = SupportPermissions(Ticket).register()
    """

    def __init__(self, model):
        self.model = model
        self.registered = False

    def get_permission_name(self, perm):
        if '.' in perm:
            return perm
        return '{app_label}.{permission_name}'.format(
            app_label=self.model._meta.app_label,
            permission_name=get_permission_codename(perm, self.model._meta))

    def get_permission_checks(self):
        permission_re = re.compile('^check_(.+?)(?!_object)_permission$')
        permissions = []
        for attr in dir(self):
            match = permission_re.match(attr)
            if match:
                permission_name = match.groups()[0]
                check = getattr(self, attr)
                # Get attribute of check to find out the permission name that
                # shall be used for this check.
                permission_name = getattr(check, 'permission_name', permission_name)
                permission_name = self.get_permission_name(permission_name)
                permissions.append((permission_name, check))
        return permissions

    def get_object_permission_checks(self):
        permission_re = re.compile('^check_(.+?)_object_permission$')
        permissions = []
        for attr in dir(self):
            match = permission_re.match(attr)
            if match:
                permission_name = match.groups()[0]
                check = getattr(self, attr)
                # Get attribute of check to find out the permission name that
                # shall be used for this check.
                permission_name = getattr(check, 'permission_name', permission_name)
                permission_name = self.get_permission_name(permission_name)
                permissions.append((permission_name, check))
        return permissions

    def register(self):
        if self.registered:
            raise RuntimeError(
                'You already tried to register {0}. You can only do this '
                'once.'.format(self))

        for permission, check in self.get_permission_checks():
            django_callable_perms.register(permission, check)
        for permission, check in self.get_object_permission_checks():
            django_callable_perms.register(permission, check, self.model)
        self.registered = True
        return self


class ModelBackendPermissions(BaseModelBackendPermissions):
    """
    Default permissions that need to exist in order to use the backend.

    We mainly fallback to django's default permission names, namely ``add``,
    ``change`` and ``delete``. In order to use this class directly, you will
    probably want to set the your ``AUTHENTICATION_BACKENDS`` setting to::

        AUTHENTICATION_BACKENDS = (
            'django_callable_perms.backends.CallablePermissionBackend',
            'django.contrib.auth.backends.ModelBackend',
        )
    """

    def check_list_permission(self, user, perm, obj):
        """Falls back to default ``change`` permission."""
        return user.has_perm(self.get_permission_name('change'))

    def check_viewlog_permission(self, user, perm, obj):
        """Falls back to default ``change`` permission."""
        return user.has_perm(self.get_permission_name('change'))

    def check_read_permission(self, user, perm, obj):
        """Falls back to default ``change`` permission."""
        return user.has_perm(self.get_permission_name('change'))

    def check_read_object_permission(self, user, perm, obj):
        """Falls back to the non-object level ``read`` permission."""
        return self.check_read_permission(user, perm, obj)

    def check_add_permission(self, user, perm, obj):
        """No custom logic, so we depend on other auth-backends to be present
        in ``settings.AUTHENTICATION_BACKENDS``."""
        return None

    def check_change_permission(self, user, perm, obj):
        """No custom logic, so we depend on other auth-backends to be present
        in ``settings.AUTHENTICATION_BACKENDS``."""
        return None

    def check_change_object_permission(self, user, perm, obj):
        """Support object level checks by falling back to the non-object level
        check."""
        return user.has_perm(self.get_permission_name('change'))

    def check_delete_permission(self, user, perm, obj):
        """No custom logic, so we depend on other auth-backends to be present
        in ``settings.AUTHENTICATION_BACKENDS``."""
        return None

    def check_delete_object_permission(self, user, perm, obj):
        """Support object level checks by falling back to the non-object level
        check."""
        return user.has_perm(self.get_permission_name('delete'))


#
# Base permissions, for all backends.


def may_access_backend(user, perm, obj):
    return user.is_staff


register(
    'django_backend.access_backend',
    may_access_backend)
