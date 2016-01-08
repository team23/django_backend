from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils import translation
from django.utils.cache import add_never_cache_headers
from django_backend.state import LANGUAGE_IDS, language, LANGUAGES
from ..ajax import DialogResponseMixin
from .permissions import BackendPermissionViewMixin


class TranslationMixin(object):
    language_url_kwarg = 'language'

    def get_translation(self):
        '''
        Sets and validates self.language_id based on the url kwargs.
        '''
        self.language_id = self.kwargs.get(self.language_url_kwarg)
        if self.language_id is not None:
            if self.language_id not in LANGUAGE_IDS:
                raise Http404
        if self.language_id is None:
            self.language_id = language.get_default()
        self.language = [lang for lang in LANGUAGES if lang[0] == self.language_id][0]

        self.backend.language.active = self.language_id
        return self.language_id

    def init_dispatch(self, request, *args, **kwargs):
        self.get_translation()
        return super(TranslationMixin, self).init_dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['languages'] = LANGUAGES
        kwargs['language_id'] = self.language_id
        kwargs['language'] = self.language
        return super(TranslationMixin, self).get_context_data(**kwargs)


class SiteMixin(object):
    site_get_param = 'site'

    def get_site(self):
        '''
        Sets and validates self.site_id based on the url kwargs.
        '''
        self.site_id = self.kwargs.get(self.site_get_param)
        self.site = None
        if self.site_id is not None:
            try:
                self.site = Site.objects.get(pk=self.site_id)
            except ValueError:
                self.site_id = None
        if self.site_id is None:
            self.site = Site.objects.get_current()
            self.site_id = self.site.pk
        self.backend.site.active = self.site_id
        return self.site_id

    def init_dispatch(self, request, *args, **kwargs):
        self.get_site()
        return super(SiteMixin, self).init_dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['sites'] = Site.objects.all()
        kwargs['site_id'] = self.site_id
        kwargs['site'] = self.site
        return super(SiteMixin, self).get_context_data(**kwargs)


class ForceEnMixin(object):
    def init_dispatch(self, request, *args, **kwargs):
        translation.activate('en')
        return super(ForceEnMixin, self).init_dispatch(request, *args, **kwargs)


class NeverCacheMixin(object):
    def dispatch(self, *args, **kwargs):
        response = super(NeverCacheMixin, self).dispatch(*args, **kwargs)
        add_never_cache_headers(response)
        return response


class BaseBackendViewMixin(object):
    backend = None

    def reverse(self, *args, **kwargs):
        return self.backend.reverse(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['backend'] = self.backend
        return super(BaseBackendViewMixin, self).get_context_data(**kwargs)

    def init_dispatch(self, request, *args, **kwargs):
        pass

    def pre_dispatch(self, request, *args, **kwargs):
        pass


class BackendViewMixin(NeverCacheMixin, DialogResponseMixin, SiteMixin,
                       TranslationMixin, BackendPermissionViewMixin,
                       BaseBackendViewMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            self.init_dispatch(request, *args, **kwargs)
            response = self.pre_dispatch(request, *args, **kwargs)
            if response:
                return response
            return super(BackendViewMixin, self).dispatch(request, *args, **kwargs)
        except PermissionDenied as exception:
            if not hasattr(self, 'handle_permission_denied'):
                raise exception
            return self.handle_permission_denied(request, exception)


class RequestFormKwargMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormKwargMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
