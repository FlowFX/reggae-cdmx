"""Reggae CDMX URL Configuration."""

from django.conf.urls import url

from reggae_cdmx import views


urlpatterns = [
    url(r'^', views.IndexView.as_view(), name='index'),
]
