from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from ..backend.views import BackendViewMixin


class IndexView(BackendViewMixin, TemplateView):
    template_name = 'django_backend/index.html'

    def get(self, request, *args, **kwargs):
        if self.kwargs.get(self.language_url_kwarg) is None:
            return HttpResponseRedirect(
                reverse('django_backend:index',
                    kwargs={
                        'site': self.site_id,
                        'language': self.language_id,
                    }))
        return super(IndexView, self).get(request, *args, **kwargs)
