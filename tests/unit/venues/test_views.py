"""Unit tests for venues.views."""
from django.urls import reverse
from mock import MagicMock

from app.venues import factories, models, views

import pytest


def test_venue_list_view(client, mocker):  # noqa: D103
    # GIVEN a number of venues
    venues = factories.VenueFactory.build_batch(5)
    mocker.patch.object(views.VenueListView, 'get_queryset', return_value=venues)

    # WHEN opening the venues list
    url = reverse('venues:list')
    response = client.get(url)

    # THEN it's there
    assert response.status_code == 200
    assert response.template_name[0] == 'venues/venue_list.html'

    # AND shows all existing venues
    for venue in venues:
        assert venue.name in response.content.decode()


@pytest.mark.parametrize(
    'url_name, venue_exists, template_name',
    [('venues:create', False, 'model_form.html'),
     ('venues:update', True, 'model_form.html'),
     ('venues:delete', True, 'model_delete.html'),
     ('venues:detail', True, 'venues/venue_detail.html'),
     ])
def test_venue_CRUD_views_GET_request_yield_200(client, mocker, url_name, venue_exists, template_name):  # noqa: D103
    # GIVEN an existing venue
    venue = factories.VenueFactory.build()
    mocker.patch.object(views.VenueDeleteView, 'get_object', return_value=venue)
    mocker.patch.object(views.VenueDetailView, 'get_object', return_value=venue)
    mocker.patch.object(views.VenueUpdateView, 'get_object', return_value=venue)

    # WHEN calling the view via GET request
    if venue_exists:
        url = reverse(url_name, args=[str(venue.id)])
    else:
        url = reverse(url_name)
    
    response = client.get(url)

    # THEN it's there
    assert response.status_code == 200
    assert response.template_name[0] == template_name


@pytest.mark.parametrize(
    'url_name, venue_exists',
    [('venues:create', False),
     ('venues:update', True),
     ('venues:delete', True),
     ])
def test_venue_CRUD_views_POST_request_redirects(client, mocker, url_name, venue_exists):  # noqa: D103
    # GIVEN an existing venue
    venue = factories.VenueFactory.build()
    mocker.patch.object(views.VenueDeleteView, 'get_object', return_value=venue)
    mocker.patch.object(views.VenueDetailView, 'get_object', return_value=venue)
    mocker.patch.object(views.VenueUpdateView, 'get_object', return_value=venue)

    mocker.patch('app.venues.models.Venue.save', MagicMock(name="save"))
    mocker.patch('app.venues.models.Venue.delete', MagicMock(name="delete"))
    # # WHEN calling the view via GET request
    if venue_exists:
        url = reverse(url_name, args=[str(venue.id)])
    else:
        url = reverse(url_name)

    data = {'name': 'Kaliman Bar'}
    response = client.post(url, data=data)
    
    # THEN we get redirected to the venues list
    assert response.status_code == 302
    assert response.url == reverse('venues:list')
