from .renderable import RenderableModelInstance


class Preview(RenderableModelInstance):
    template_name = (
        'django_backend/{app_label}/_{object_name}_preview.html',
        'django_backend/_object_preview.html',
    )
