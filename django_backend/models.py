# Our goal is to auto-load all the default backends when Django starts up.
# The preferred way to do so would be in DjangoBackendConfig.ready
# But when using an old Django version we have to rely on the loading of
# this models.py
try:
    import django.apps  # noqa
except ImportError:
    from .autoload import autoload_backends

    autoload_backends()
