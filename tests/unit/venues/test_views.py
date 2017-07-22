"""Unit tests for venues.views."""
from django.urls import reverse
from mock import patch, MagicMock

from app.venues import factories, views


def test_venue_list_view(rf):  # noqa: D103, E302
    venues = factories.VenueFactory.build_batch(5)

    # GIVEN a couple mock venues
    with patch.object(views.VenueListView, 'get_queryset', return_value=venues):

        url = reverse('venues:list')
        request = rf.get(url)
        response = views.VenueListView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'venues/venue_list.html'

        response.render()
        content = response.rendered_content

        for venue in venues:
            assert venue.name in content


def test_venue_create_view_GET(rf):  # noqa: D103

    url = reverse('venues:create')

    request = rf.get(url)
    response = views.VenueCreateView.as_view()(request)

    assert response.template_name[0] == 'model_form.html'
    assert response.status_code == 200

    response.render()
    assert 'submit' in response.rendered_content


@patch('app.venues.models.Venue.save', MagicMock(name="save"))
def test_venue_create_view_POST(client):  # noqa: D103
    # GIVEN any state
    # use the client for the messages middleware that rf does not provide
    # WHEN creating a new venue
    url = reverse('venues:create')
    response = client.post(url, data={'name': 'Kaliman Bar'})
    # response = views.VenueCreateView.as_view()(request)

    # THEN we get redirected to the venues list
    assert response.status_code == 302
    assert response.url == reverse('venues:list')


def test_venue_update_view_GET(rf):  # noqa: D103
    venue = factories.VenueFactory.build()

    with patch.object(views.VenueUpdateView, 'get_object', return_value=venue):

        url = reverse('venues:update', args=[str(venue.id)])
        request = rf.get(url)
        response = views.VenueUpdateView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'model_form.html'

        response.render()


# @patch('app.venues.models.Venue.save', MagicMock(name="save"))
def test_venue_update_view_POST(client, rf):  # noqa: D103
    venue = factories.VenueFactory.build()

    with patch.object(views.VenueDeleteView, 'get_object', return_value=venue):

        url = reverse('venues:update', args=[str(venue.id)])
        request = rf.post(url)  # noqa
        # response = views.VenueUpdateView.as_view()(request)
        # TODO: finish update view POST test

        # assert response.status_code == 302
        # assert response.url == reverse('venues:list')


def test_venue_delete_view_GET(rf):  # noqa: D103
    venue = factories.VenueFactory.build()

    with patch.object(views.VenueDeleteView, 'get_object', return_value=venue):

        url = reverse('venues:delete', args=[0])
        request = rf.get(url)

        response = views.VenueDeleteView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'model_delete.html'

        response.render()


@patch('app.venues.models.Venue.delete', MagicMock(name="delete"))
def test_venue_delete_view_POST(client, rf):  # noqa: D103
    venue = factories.VenueFactory.build()

    with patch.object(views.VenueDeleteView, 'get_object', return_value=venue):

        url = reverse('venues:delete', args=[0])
        response = client.post(url)

        # TODO: add messages middleware to request factory
        # request = rf.post(url)
        # response = views.VenueDeleteView.as_view()(request)

        assert response.status_code == 302
        assert response.url == reverse('venues:list')


def test_venue_detail_view(rf):  # noqa: D103
    venue = factories.VenueFactory.build()

    with patch.object(views.VenueDetailView, 'get_object', return_value=venue):
        url = reverse('venues:detail', args=[0])
        request = rf.get(url)

        response = views.VenueDetailView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'venues/venue_detail.html'

        response.render()
        content = response.rendered_content

        assert venue.name in content
