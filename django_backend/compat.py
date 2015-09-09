import django

if django.VERSION > (1, 8):
    from django.contrib.admin.utils import NestedObjects  # noqa
else:
    from django.contrib.admin.util import NestedObjects  # noqa


def get_template_name(template):
    if django.VERSION > (1, 8):
        return template.template.name
    else:
        return template.name
