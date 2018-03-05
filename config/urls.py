"""Reggae CDMX URL Configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseNotFound
from django.urls import include, path

from app.events.views import HomePage

from django.views.generic import RedirectView, TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path(r'^', include('django.contrib.auth.urls')),
    path('accounts/signup/', HttpResponseNotFound),
    path('accounts/', include('allauth.urls')),
    path(
        'accounts/profile/',
        TemplateView.as_view(template_name='account/profile.html'),
        name="account_profile",
    ),
    path('', HomePage.as_view(), name='index'),
    # Events
    path('events/', include('app.events.urls', namespace='events')),
    # Venues
    path('venues/', include('app.venues.urls', namespace='venues')),
]


# Permanent redirects
urlpatterns += [
    path('login/', RedirectView.as_view(url='/accounts/login/', permanent=True)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] \
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
        + urlpatterns
