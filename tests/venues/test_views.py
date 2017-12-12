"""Unit tests for venues.views."""
from django.urls import reverse

from app.venues import factories, views

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
def test_CRUD_views_GET_yields_200(client, mock_venue, url_name, venue_exists, template_name):  # noqa: D103
    # GIVEN an existing venue
    # WHEN calling the view via GET request
    if venue_exists:
        url = reverse(url_name, args=[str(mock_venue.id)])
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
def test_venue_CRUD_views_POST_request_redirects(client, mock_venue, url_name, venue_exists):  # noqa: D103
    # GIVEN an existing venue
    # WHEN calling the view via GET request
    if venue_exists:
        url = reverse(url_name, args=[str(mock_venue.id)])
    else:
        url = reverse(url_name)

    data = {'name': 'Kaliman Bar'}
    response = client.post(url, data=data)

    # THEN we get redirected to the venues list
    assert response.status_code == 302
    assert response.url == reverse('venues:list')