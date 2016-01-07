from collections import OrderedDict
from django.conf.urls import include, url
from django.contrib.auth import get_permission_codename
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django_viewset import ViewSet, ModelViewSet
from floppyforms.__future__.models import ModelForm, modelform_factory

from ..forms import formfield_callback
from ..group import Group
from .preview import Preview
from .inline_related import InlineRelatedObject
from .columns import BackendColumn
from .forms import ActionForm, SortForm
from .urlname_helper import URLNames
from .utils import TemplateHintProvider


DEFAULT_REGISTRY = 'default'


class BaseBackend(TemplateHintProvider, ViewSet):
    # Import the branch and language globals here to make them available as
    # class attributes. This is useful, so that view instances that have a
    # ``self.backend`` variable attached don't need to import from django_backend.
    # This is needed in some circumstances to prevent circular imports.
    from django_backend.state import language
    from django_backend.state import site

    namespace = 'django_backend'
    verbose_name = None
    verbose_name_plural = None

    template_hint = None

    def __init__(self, id, verbose_name=None, verbose_name_plural=None,
                 parent=None, registry=DEFAULT_REGISTRY, group=None):
        self.id = id
        if verbose_name:
            self.verbose_name = verbose_name
        if verbose_name_plural:
            self.verbose_name_plural = verbose_name_plural
        self.parent = parent

        self.registry = registry
        self.group = group
        self._registries = {}
        self._groups = {}
        self.base = self
        while self.base and self.base.parent:
            self.base = self.base.parent
        urlname_prefix = self.get_urlname_prefix()
        super(BaseBackend, self).__init__(urlname_prefix=urlname_prefix)

    def __repr__(self):
        id = self.id
        parent = self.parent
        while parent:
            id = parent.id + '.' + id
            parent = parent.parent
        return '<{0}: {1}>'.format(
            self.__class__.__name__,
            id)

    def reverse(self, viewname, urlconf=None, args=None, kwargs=None, prefix=None, current_app=None):
        from django.contrib.sites.models import Site

        if kwargs is None:
            kwargs = {}
        kwargs.setdefault('site', Site.objects.get_current().pk)
        kwargs.setdefault('language', self.language.active)
        return reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs, prefix=prefix, current_app=current_app)

    def get_template_hints(self, name_provider, hint_providers):
        return [self.template_hint] + self.FEATURES.keys()

    def register(self, backend_class, registry=DEFAULT_REGISTRY,
                 group=None, **kwargs):
        """
        Enables nested backends. There are two different registries in use. The
        argument `registry` is refering to a internal categorization. Usually a
        backend goes into the 'default' registry, but there are special cases
        like backends only used for inline-edit modals. Those should have a
        extra registry, so that they live in a extra url-namespace etc.

        The other registry is the called `group`. This is only used in the
        frontend to categorize backends by there relations. It's for example
        used to group the backends into the different boxes in the sidebar.
        """
        backend = backend_class(
            parent=self,
            registry=registry,
            group=group,
            **kwargs)
        self._registries.setdefault(registry, []).append(backend)
        if group is not None:
            group = self.get_group(group)
            group.append(backend)
        return backend

    def get_group(self, id):
        """
        Get a registered group by id. If it is not yet registered, it will
        create a new group with the given ID and register this. If a existing
        group is given, it will be reused and registered if it is not yet
        already.
        """
        if isinstance(id, Group):
            group = id
        elif id in self._groups:
            group = self._groups[id]
        else:
            group = Group(id)
        if group.id not in self._groups:
            self._groups[group.id] = group
        return group

    def get_registered(self, registry=DEFAULT_REGISTRY, include_children=True):
        backends = []
        if registry in self._registries:
            backends.extend(self._registries[registry])
        if include_children:
            for child in self._registries.get(registry, []):
                backends.extend(
                    child.get_registered(registry, include_children=include_children))
        return backends

    def find(self, id=None, model=None, registry=DEFAULT_REGISTRY):
        """
        Find a backend with the given ``id`` which is registered in
        ``registry``.

        The logic is to look inside the backend you call this method on if there
        is a backend that matches. If that's not the case than go up to the
        parent and try on this level.
        """

        assert id or model, 'Either provide ``id`` or ``model``.'
        if registry in self._registries:
            backend_list = self._registries[registry]
            for backend in backend_list:
                id_matches = id and backend.id == id
                backend_model = getattr(backend, 'model', None)
                model_matches = model and backend_model == model
                if id_matches or model_matches:
                    return backend
        if self.parent:
            try:
                return self.parent.find(
                    id=id,
                    model=model,
                    registry=registry)
            except ValueError:
                pass
        raise ValueError(
            'Cannot find a backend with id `{0}` or model `{1}` in the '
            'registry `{2}`'.format(
                id,
                model,
                registry))

    def __getitem__(self, key):
        '''
        Allow lookups by backend id:

        >>> backend['menu']
        <MenuBackend: menu>
        '''
        try:
            return self.find(id=key)
        except ValueError as e:
            raise KeyError(e.args[0])

    @property
    def urlnames(self):
        return URLNames(self)

    def get_urlname_prefix(self):
        prefix = self.id
        if self.registry != DEFAULT_REGISTRY:
            prefix = (
                self.registry +
                self.urlname_separator +
                prefix)
        if self.parent and self.parent.urlname_prefix:
            prefix = (
                self.parent.urlname_prefix +
                self.urlname_separator +
                prefix)
        return prefix

    def get_view_kwargs(self, viewset_view):
        kwargs = super(BaseBackend, self).get_view_kwargs(viewset_view)
        if hasattr(viewset_view.view, 'backend'):
            kwargs['backend'] = self
        return kwargs

    @property
    def groups(self):
        return sorted(
            self._groups.values(),
            key=lambda g: g.position)

    def get_children_urls(self):
        '''
        Return the urls of all registered backends.
        '''
        urls = []
        for registry, backends in self._registries.items():
            for backend in backends:
                regex = r'^{0}{1}/'.format(
                    registry + '/' if registry != DEFAULT_REGISTRY else '',
                    backend.id)
                urls.append(
                    url(regex, include(backend.get_urls())))
        return urls

    def get_urls(self):
        viewset_urls = super(BaseBackend, self).get_urls()
        urls = viewset_urls + self.get_children_urls()
        return urls

    def get_features(self):
        return {}  # none (so far)

    @property
    def FEATURES(self):
        try:
            return self._FEATURES
        except AttributeError:
            self._FEATURES = self.get_features()
            return self._FEATURES

    def has_perm(self, user, perm, obj=None):
        # If it does not have a '.' in the permission name (like 'list'), it
        # wants to check for a model permission. So we user the access_backend
        # instead since the index has no 'list' permission assigned.
        if '.' not in perm:
            return user.has_perm('django_backend.access_backend')
        else:
            return user.has_perm(perm, obj)


class BaseModelBackend(ModelViewSet, BaseBackend):
    form_class = ModelForm
    filter_form_class = None
    action_form_class = ActionForm
    sort_form_class = SortForm
    paginate_by = 12
    order_by = None
    readonly_fields = ()

    preview = Preview()
    inline_related_object = InlineRelatedObject()

    def __init__(self, *args, **kwargs):
        ModelViewSet.__init__(self, model=kwargs.pop('model'))
        BaseBackend.__init__(self, *args, **kwargs)

        self.model_opts = self.model._meta
        if not self.verbose_name:
            self.verbose_name = self.model._meta.verbose_name
        if not self.verbose_name_plural:
            self.verbose_name_plural = self.model._meta.verbose_name_plural

    def get_queryset(self):
        return self.model._default_manager.all()

    def prepare_origin(self, origin):
        return origin

    def prepare_object(self, origin, object):
        return object

    def save_object(self, origin, object):
        object.save()
        return object

    def dismiss_object(self, origin, object):
        return object

    def delete_object(self, object):
        object.delete()

    def get_to_be_deleted_objects(self, objects, user):
        # Most of this code is ripped of
        # ``django.contrib.admin.util.get_deleted_objects`` with some changes
        # to better integrate it with django_backend.
        from django_backend.compat import NestedObjects

        using = 'default'

        collector = NestedObjects(using=using)
        collector.collect(objects)
        perms_needed = set()

        backend = self

        def format_callback(obj):
            try:
                obj_backend = backend.find(model=obj.__class__)
            except ValueError:
                obj_backend = None

            if obj_backend:
                if not obj_backend.has_perm(user=user, perm='delete', obj=obj):
                    perms_needed.add(obj._meta.verbose_name)

            return {
                'backend': obj_backend,
                'object': obj,
                'user': user
            }

        to_delete = collector.nested(format_callback)
        protected = [format_callback(obj) for obj in collector.protected]
        return to_delete, perms_needed, protected

    def has_perm(self, user, perm, obj=None):
        if '.' not in perm:
            perm = '{app_label}.{permission_name}'.format(
                app_label=self.model_opts.app_label,
                permission_name=get_permission_codename(perm, self.model_opts))
        return user.has_perm(perm, obj)

    def get_form_initial(self, object):
        return {}

    def get_form_class(self, object=None, form_class=None):
        return modelform_factory(
            self.model,
            form=form_class or self.form_class,
            formfield_callback=formfield_callback)

    def get_preview(self, object):
        from django.utils import translation

        with translation.override(self.language.active):
            return self.preview.render({'object': object})

    def get_list_actions(self):
        return {}

    def get_available_list_actions(self, user):
        '''
        Returns the actions defined by ``get_list_actions``, sorted by position
        and filtered by permission.
        '''
        available_actions = []
        for name, action in self.get_list_actions().items():
            if action.check_permission(backend=self, user=user):
                available_actions.append((name, action))
        return OrderedDict(
            list(sorted(
                available_actions,
                key=lambda action_tuple: action_tuple[1].position)))

    def get_action_form_class(self):
        return self.action_form_class

    def get_filter_form_class(self):
        return self.filter_form_class

    def get_sort_form_class(self):
        return self.sort_form_class

    def get_list_columns(self):
        return {
            'name': BackendColumn(
                _('Name'),
                'django_backend/columns/_name.html',
                position=0),
            'buttons': BackendColumn(
                '',
                'django_backend/columns/_buttons.html', position=1000),
        }

    @property
    def list_columns(self):
        return OrderedDict(list(sorted(self.get_list_columns().items(), cmp=lambda x,y: cmp(x[1].position, y[1].position))))

    def get_select_columns(self):
        return {
            'name': BackendColumn(
                _('Name'),
                'django_backend/columns/_plain_name.html',
                position=0),
            'select': BackendColumn(
                '',
                'django_backend/columns/_select.html', position=1000),
        }

    @property
    def select_columns(self):
        return OrderedDict(list(sorted(self.get_select_columns().items(), cmp=lambda x,y: cmp(x[1].position, y[1].position))))

    def get_form_tab_definition(self):
        return {}

    def get_form_tabs(self, form):
        tab_definition = self.get_form_tab_definition()
        self.add_fallback_form_fields(tab_definition, form)
        tab_definition_tuples = (
            (key, tab)
            for key, tab in tab_definition.items()
            if tab.rows)
        return OrderedDict(
            sorted(
                tab_definition_tuples,
                key=lambda t: t[1].position))

    def add_fallback_form_fields(self, tab_definition, form):
        from .form_tabs import FormTab

        if not 'content' in tab_definition:
            tab_definition['content'] = FormTab(
                _('Content'),
                [])
        self.add_fallback_form_fields_to_tab(tab_definition['content'], tab_definition, form)

    def add_fallback_form_fields_to_tab(self, tab, tab_definition, form):
        from .form_tabs import FormRow, FormField

        tabs_fields = []
        for _tab in tab_definition.values():
            tabs_fields = tabs_fields + _tab.fields
        tabs_fieldnames = [f.field for f in tabs_fields if hasattr(f, 'field')]
        for form_fieldname, form_field in form.fields.items() + form.composite_fields.items():
            if form_fieldname in tabs_fieldnames:
                continue
            if form_field.widget.is_hidden:
                continue
            tab._rows.append(FormRow(form_field.label, [
                FormField(form_fieldname)
            ]))
            tabs_fieldnames.append(form_fieldname)

    def get_readonly_fields(self, form, object):
        """
        Return the readonly fields. You can override this to mark some fields
        as readonly depending on the form or object. By default it returns the
        list given in the ``readonly_fields`` attribute.

        For example you can use it to make fields only editable during
        creation. Those that are then edited can then marked as readonly.
        """
        return list(self.readonly_fields)
