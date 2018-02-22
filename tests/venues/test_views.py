"""Unit tests for venues.views."""
from app.venues import factories, views

from django.urls import reverse

import pytest


class TestAnonymousAccess:
    """Test limited access of anonymous users."""

    @pytest.mark.parametrize(
        'url_name, venue_exists', [
            ('venues:create', False),
            ('venues:detail', True),
            ('venues:update', True),
            ('venues:delete', True),
        ])
    def test_anonymous_user_cant_access_create_read_update_delete(self, client, mock_venue, url_name, venue_exists):
        # GIVEN an existing venue
        # WHEN requesting the venue create/update/delete view as an anonymous user
        if venue_exists:
            url = reverse(url_name, kwargs={'pk': mock_venue.id})
        else:
            url = reverse(url_name)

        response = client.get(url)

        # THEN she gets redirected to the login page
        assert response.status_code == 302
        assert response.url.startswith(reverse('account_login'))


class TestVenuesListView:
    """Test venues.views.VenueListView on '/venues/'."""

    url = reverse('venues:list')

    def test_anonymous_users_cant_access_venues_list(self, client, mocker):  # noqa: D102
        # GIVEN any state
        mocker.patch.object(views.VenueListView, 'get_queryset', return_value=None)

        # WHEN requesting the venues list as an anonymous user
        response = client.get(self.url)

        # THEN she gets redirected to the login page
        assert response.status_code == 302
        assert response.url.startswith(reverse('account_login'))

    def test_venue_list_shows_existing_venues(self, client, authenticated_user, mocker):  # noqa: D102
        # GIVEN a number of venues
        venues = factories.VenueFactory.build_batch(3, id=9999)
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
def test_CRUD_views_GET_yields_200(client, authenticated_user, mock_venue, url_name, venue_exists, template_name):  # noqa: D103
    # GIVEN an existing venue
    # WHEN calling the CRUD views as an authenticated user
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
def test_venue_CRUD_views_POST_request_redirects(client, authenticated_user, mock_venue, url_name, venue_exists):  # noqa: D103
    # GIVEN an existing venue
    # WHEN creating/updating/deleting a venue as an authenticated user
    if venue_exists:
        url = reverse(url_name, args=[str(mock_venue.id)])
    else:
        url = reverse(url_name)

    data = {'name': 'Kaliman Bar'}
    response = client.post(url, data=data)

    # THEN we get redirected to the venues list
    assert response.status_code == 302
    assert response.url == reverse('venues:list')
