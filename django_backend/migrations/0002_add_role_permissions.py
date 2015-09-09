# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_role_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth', 'Permission')

    group_ct, created = ContentType.objects.get_or_create(
        app_label='auth',
        model='group')

    Permission.objects.get_or_create(
        content_type=group_ct,
        name='Has editor permissions',
        codename='editor_permission')

    Permission.objects.get_or_create(
        content_type=group_ct,
        name='Has chief editor permissions',
        codename='chief_editor_permission')

    Permission.objects.get_or_create(
        content_type=group_ct,
        name='Has admin permissions',
        codename='admin_permission')


def remove_role_permissions(apps, schema_editor):
    Permission = apps.get_model('auth', 'Permission')
    auth_permissions = Permission.objects.filter(
        content_type__app_label='auth',
        content_type__model='group')
    auth_permissions.filter(codename='editor_permission').delete()
    auth_permissions.filter(codename='chief_editor_permission').delete()
    auth_permissions.filter(codename='admin_permission').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('django_backend', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(
            create_role_permissions,
            remove_role_permissions,
        ),
    ]
