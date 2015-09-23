from ..utils import TemplateHintProvider, TemplateNameProvider
from .base import BackendViewMixin, RequestFormKwargMixin


class BackendModelViewMixin(
        TemplateNameProvider,
        TemplateHintProvider,
        RequestFormKwargMixin,
        BackendViewMixin):

    '''
    A base view mixin that shall be used for all views that handle a model of
    some kind, e.g. create/update/list views.

    It determines a list of the template names that are checked in order to
    find the most suitable one.

    For example the update view for the mcpage.Page model try to use the
    templates in this order:

    * ``django_backend/mcpage/page_update.html``
    * ``django_backend/object_update.html``

    The first one includes the app_label and the model's name. The ``update``
    part of the name is determined by the ``template_type`` attribute on
    the view.

    The second one is the hardcoded name set with the ``template_name``
    attribute on the view.
    '''

    context_object_name = 'object'

    default_template_name = 'django_backend/' \
                            '{%if type == "partial"%}_{%endif%}' \
                            'object_{{type}}' \
                            '{%if hint%}_{{hint}}{%endif%}' \
                            '.html'
    template_name = 'django_backend/' + TemplateNameProvider.template_name

    template_hint = None
    template_type = None

    def get_template_hints(self, name_provider, hint_providers):
        return [self.template_hint]

    def get_template_names(self):
        kwargs = {
            'type': self.template_type
        }
        hint_providers = [self, self.backend]
        template_names = super(BackendModelViewMixin, self).get_template_names(
            hint_providers=hint_providers, **kwargs)
        default_template_names = super(BackendModelViewMixin, self).get_template_names(
            template_name=self.default_template_name,
            hint_providers=hint_providers,
            **kwargs)
        return template_names + default_template_names

    def get_app_label(self):
        return self.model._meta.app_label.lower()

    def get_model_name(self):
        return self.model._meta.object_name.lower()

    def get_queryset(self):
        return self.backend.get_queryset()

    def get_context_data(self, **kwargs):
        kwargs['opts'] = self.backend.model._meta
        return super(BackendModelViewMixin, self).get_context_data(**kwargs)

    def get_preview(self, object):
        return self.backend.get_preview(object)

    def get_inline_related_object_preview(self, object):
        return self.backend.inline_related_object.render({
            'object': object,
            'backend': self.backend,
            'user': self.request.user,
        })

    def get_read_url(self, object):
        '''
        Get the url to the read view. If the user does not have the sufficient
        permission we provide some fallbacks so that we can redirect the user in every case to a page that kind of makes sense.
        '''
        if self.has_perm('read', object):
            urlname = self.backend.urlnames.views['read'].name
            return self.reverse(urlname, kwargs={
                'pk': object.pk,
            })
        if self.has_perm('list'):
            urlname = self.backend.urlnames.views['index'].name
            return self.reverse(urlname)
        urlname = self.backend.base.urlnames.views['index'].name
        return self.reverse(urlname)

    def get_update_url(self, object):
        if self.has_perm('change', object):
            urlname = self.backend.urlnames.views['update'].name
            return self.reverse(urlname, kwargs={
                'pk': object.pk,
            })
        # Fall back to read url if we don't have the permission for update
        # view.
        return self.get_read_url(object=object)

    def get_list_url(self):
        if self.has_perm('list'):
            urlname = self.backend.urlnames.views['index'].name
            return self.reverse(urlname)
        urlname = self.backend.base.urlnames.views['index'].name
        return self.reverse(urlname)

    def get_permission_denied_redirect_url(self):
        return self.get_list_url()


class BackendSingleObjectMixin(BackendModelViewMixin):
    form_class = None

    def prepare_object(self, origin):
        return origin

    def get_origin(self, *args, **kwargs):
        return super(BackendSingleObjectMixin, self).get_object(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        if not hasattr(self, 'object'):
            self.origin = self.get_origin()
            self.object = self.prepare_object(self.origin)
        return self.object

    def get_context_data(self, **kwargs):
        kwargs['origin'] = self.origin
        return super(BackendSingleObjectMixin, self).get_context_data(**kwargs)

    def get_form_class(self):
        '''
        Return the form class provided by the backend. It will be overriden if
        the view defines a ``form_class`` attribute itself.

        Use this to provide a custom form class in the ``URLView`` definition
        like::

            class MyBackend(...):
                create = URLView(
                    r'^add/$',
                    BackendCreateView,
                    view_kwargs={'form_class': MyCustomForm})
        '''

        return self.backend.get_form_class(
            object=self.get_object(),
            form_class=self.form_class)

    def get_json(self, **kwargs):
        json_data = super(BackendSingleObjectMixin, self).get_json(**kwargs)
        return json_data
