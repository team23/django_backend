from django.conf.urls import include, patterns, url

from django_backend import site


urlpatterns = patterns(
    '',
    url(r'^backend/', include(site.get_urls(), namespace='django_backend')),
)
