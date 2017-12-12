"""Reggae CDMX URL Configuration."""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from app.events.views import IndexView

from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path(r'^', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path(
        'accounts/profile/',
        TemplateView.as_view(template_name='account/profile.html'),
        name="account_profile",
    ),
    path('', IndexView.as_view(), name='index'),
    # Events
    path('events/', include('app.events.urls', namespace='events')),
    # Venues
    path('venues/', include('app.venues.urls', namespace='venues')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
