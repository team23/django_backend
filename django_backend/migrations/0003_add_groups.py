# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_groups(apps, schema_editor):
    Permission = apps.get_model('auth', 'Permission')
    auth_permissions = Permission.objects.filter(
        content_type__app_label='auth',
        content_type__model='group')
    editor_permission = auth_permissions.get(codename='editor_permission')
    chief_editor_permission = auth_permissions.get(codename='chief_editor_permission')
    admin_permission = auth_permissions.get(codename='admin_permission')

    Group = apps.get_model('auth', 'Group')

    editor, __ = Group.objects.get_or_create(name='editor')
    editor.permissions.add(editor_permission)
    chief_editor, __ = Group.objects.get_or_create(name='chief editor')
    chief_editor.permissions.add(editor_permission, chief_editor_permission)
    admin, __ = Group.objects.get_or_create(name='admin')
    admin.permissions.add(editor_permission, chief_editor_permission, admin_permission)


def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['editor', 'chief editor', 'admin']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('django_backend', '0002_add_role_permissions'),
    ]

    operations = [
        migrations.RunPython(
            create_groups,
            remove_groups,
        ),
    ]
