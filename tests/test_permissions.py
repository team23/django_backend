from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.test import TestCase

from .models import PermissionTestModel


class PermissionTests(TestCase):
    def setUp(self):
        self._user = User.objects.create(username='user')

    @property
    def user(self):
        """Always reload user in order to prevent caching in user_permissions
        attribute."""
        return User.objects.get(pk=self._user.pk)

    def test_list_permission(self):
        self.assertFalse(self.user.has_perm('tests.list_permissiontestmodel'))

        # The default list permission depends on the change permission.
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_permissiontestmodel'))

        self.assertTrue(self.user.has_perm('tests.list_permissiontestmodel'))

    def test_add_permission(self):
        self.assertFalse(self.user.has_perm('tests.add_permissiontestmodel'))

        self.user.user_permissions.add(
            Permission.objects.get(codename='add_permissiontestmodel'))

        self.assertTrue(self.user.has_perm('tests.add_permissiontestmodel'))

    def test_change_permission(self):
        instance = PermissionTestModel.objects.create()

        self.assertFalse(self.user.has_perm('tests.change_permissiontestmodel'))
        self.assertFalse(self.user.has_perm('tests.change_permissiontestmodel', instance))

        self.user.user_permissions.add(
            Permission.objects.get(codename='change_permissiontestmodel'))

        self.assertTrue(self.user.has_perm('tests.change_permissiontestmodel'))
        self.assertTrue(self.user.has_perm('tests.change_permissiontestmodel', instance))

    def test_delete_permission(self):
        instance = PermissionTestModel.objects.create()

        self.assertFalse(self.user.has_perm('tests.delete_permissiontestmodel'))
        self.assertFalse(self.user.has_perm('tests.delete_permissiontestmodel', instance))

        self.user.user_permissions.add(
            Permission.objects.get(codename='delete_permissiontestmodel'))

        self.assertTrue(self.user.has_perm('tests.delete_permissiontestmodel'))
        self.assertTrue(self.user.has_perm('tests.delete_permissiontestmodel', instance))
