"""Unit tests for venues.views."""
from django.urls import reverse
from mock import MagicMock

from app.venues import factories, models, views

import pytest


@pytest.mark.parametrize(
    'url_name, venue_exists, template_name',
    [('venues:create', False, 'model_form.html'),
     ('venues:update', True, 'model_form.html'),
     ('venues:delete', True, 'model_delete.html'),
     ('venues:detail', True, 'venues/venue_detail.html'),
     ])
def test_venues_views_GET_request_yield_200(client, mocker, url_name, venue_exists, template_name):  # noqa: D103
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


def test_venue_create_view_POST_redirects_to_venue_list(client, mocker):  # noqa: D103
    # GIVEN any state
    mocker.patch('app.venues.models.Venue.save', MagicMock(name="save"))

    # WHEN creating a new venue via POST request
    url = reverse('venues:create')
    response = client.post(url, data={'name': 'Kaliman Bar'})

    # THEN we get redirected to the venues list
    assert response.status_code == 302
    assert response.url == reverse('venues:list')


def test_venue_create_view_POST_creates_new_venue(db, client):  # noqa: D103
    # GIVEN an empty database
    assert models.Venue.objects.count() == 0

    # WHEN creating a new venue via POST request
    url = reverse('venues:create')
    client.post(url, data={'name': 'Roxy Bar'})

    # THEN it gets saved to the database
    assert models.Venue.objects.count() == 1


def test_venue_update_view_POST_redirects_to_list_view(client, mocker):  # noqa: D103
    # GIVEN an existing venue
    venue = factories.VenueFactory.build()
    mocker.patch.object(views.VenueUpdateView, 'get_object', return_value=venue)
    mocker.patch('app.venues.models.Venue.save', MagicMock(name="save"))

    # WHEN updating the venue via POST request
    url = reverse('venues:update', args=[str(venue.id)])
    response = client.post(url, data={'name': 'Roxy Bar'})

    # THEN it redirects to the venues list
    assert response.status_code == 302
    assert response.url == reverse('venues:list')


def test_venue_delete_view_POST_redirects_to_venues_list(client, mocker):  # noqa: D103
    # GIVEN an existing venue
    venue = factories.VenueFactory.build()
    mocker.patch.object(views.VenueDeleteView, 'get_object', return_value=venue)
    mocker.patch('app.venues.models.Venue.delete', MagicMock(name="delete"))

    # WHEN deleting the venue via POST request
    url = reverse('venues:delete', args=[str(venue.id)])
    response = client.post(url)

    # THEN we get redirected to the venues list
    assert response.status_code == 302
    assert response.url == reverse('venues:list')

