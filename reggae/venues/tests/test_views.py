from django.urls import reverse
from mock import patch

from reggae.venues.factories import VenueFactory
from reggae.venues.views import (VenueCreateView, VenueDeleteView,
                                 VenueListView,
                                 VenueUpdateView,
                                 )


def test_venue_list_view(rf):  # noqa: D103, E302
    venues = VenueFactory.build_batch(5)

    # GIVEN a couple mock venues
    with patch.object(VenueListView, 'get_queryset', return_value=venues):

        url = reverse('venues:list')
        request = rf.get(url)
        response = VenueListView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'venue_list.html'

        response.render()
        content = response.rendered_content

        for venue in venues:
            assert venue.name in content


def test_venue_create_view(rf):  # noqa: D103

    url = reverse('venues:create')

    request = rf.get(url)
    response = VenueCreateView.as_view()(request)
    assert response.template_name[0] == 'model_form.html'

    response.render()
    assert 'submit' in response.rendered_content


def test_venue_update_view(rf):  # noqa: D103
    venue = VenueFactory.build()

    with patch.object(VenueUpdateView, 'get_object', return_value=venue):

        url = reverse('venues:update', args=[str(venue.id)])
        request = rf.get(url)
        response = VenueUpdateView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'model_form.html'

        response.render()


def test_venue_delete_view(rf):  # noqa: D103
    venue = VenueFactory.build()

    with patch.object(VenueDeleteView, 'get_object', return_value=venue):

        url = reverse('venues:delete', args=[0])
        request = rf.get(url)

        response = VenueDeleteView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'model_delete.html'

        response.render()
