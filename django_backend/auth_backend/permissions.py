from django.contrib.auth.models import User, Group

from ..permissions import ModelBackendPermissions


class SuperUserOnlyPermissions(ModelBackendPermissions):
    def check_list_permissions(self, user, perm, obj):
        return user.has_perm('auth.admin_permission')

    def check_viewlog_permissions(self, user, perm, obj):
        return user.has_perm('auth.admin_permission')

    def check_add_permissions(self, user, perm, obj):
        return user.has_perm('auth.admin_permission')

    def check_read_permissions(self, user, perm, obj):
        return user.has_perm('auth.admin_permission')

    def check_change_permissions(self, user, perm, obj):
        return user.has_perm('auth.admin_permission')

    def check_delete_permissions(self, user, perm, obj):
        return user.has_perm('auth.admin_permission')


SuperUserOnlyPermissions(User).register()
SuperUserOnlyPermissions(Group).register()
