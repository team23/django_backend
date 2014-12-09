class URLNames(object):
    '''
    This is a helper class to create urlnames for backend views dynamically in
    the templates. You can use it in the template as follows::

        {% url backend.urlnames.views.create.name %}

    In the example ``{{ backend.urlnames.views.create.name }}`` would return
    something like ``"django_backend:page-create"``.

    The benefit of using the helper is that you can use the same template for
    all backends because the urlnames are constructed dynamically. The backend
    templates always contain the ``{{ backend }}`` variable which is the
    backend for the currently active active url (e.g. the page backend, menu
    backend, base backend ...).

    The three last bits on the urlnames helper variable is always the literal
    ``views``, then the view name, followed by either ``name`` or ``url``::

        Access the urlname of the update view (and adding necessary url
        arguments):
        {% url backend.urlnames.views.update.name language=language_id pk=object.pk%}

        Access the absolute url of the view called ``index``:
        {{ backend.urlnames.views.index.url }}

        That's only rarely useful in the backend's context, since this does
        not accept url arguments.

    Before naming the view you can traverse the backends a bit to reference
    another backend if necessary. Therefore use the name of a registry::

        {% url backend.urlnames.inline.views.update.name pk=... %}

        This will give you the name of the update view of the backend with the
        same model as the active backend but which is registered in the
        ``inline`` registry.

    You can also use the attributes on the backend itself to traverse the
    backend tree and then call the urlnames helper there. For example if you
    want to call the index view of the base backend::

        {% url backend.base.urlnames.views.index.name %}
    '''

    def __init__(self, backend, trail=None, view_name=None):
        self.backend = backend
        self.trail = trail
        self.view_name = view_name

    @property
    def name(self):
        if self.view_name:
            view = self.backend.get_view(self.view_name)
            urlname = '{0}:{1}'.format(
                self.backend.namespace,
                self.backend.get_view_urlname(view))
            return urlname

    @property
    def url(self):
        if self.name:
            return self.backend.reverse(self.name)

    @property
    def views(self):
        return self.__class__(self.backend, trail='views')

    def __unicode__(self):
        return unicode(self.name or '')

    def __getitem__(self, key):
        if self.trail == 'views':
            if self.view_name:
                if key == 'name':
                    return self.name
                elif key == 'url':
                    return self.url
            else:
                return self.__class__(
                    self.backend,
                    trail=self.trail,
                    view_name=key)

        if hasattr(self, key):
            return getattr(self, key)

        # It was not a view name, or a valid attribute, so we assume it's the
        # name of a registry.
        try:
            backend = self.backend.find(self.backend.id, key)
            return self.__class__(backend)
        except ValueError:
            pass

        return None
