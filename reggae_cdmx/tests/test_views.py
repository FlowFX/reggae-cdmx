"""Unit tests for calendar views."""
from django.urls import reverse

from mock import patch

from reggae_cdmx.factories import EventFactory, VenueFactory

from reggae_cdmx.views import (IndexView,
                               EventCreateView, EventDeleteView,
                               EventDetailView, EventListView,
                               EventUpdateView,
                               VenueCreateView, VenueDeleteView,
                               VenueListView,
                               VenueUpdateView,
                               )


""" EVENT VIEWS """
def test_index_view_with_no_events(rf):  # noqa: D103, E302
    # GIVEN the home page
    url = reverse('index')

    # WHEN calling
    request = rf.get(url)
    response = IndexView.as_view()(request)

    # THEN it's there,
    assert response.status_code == 200
    assert response.template_name[0] == 'index.html'
    assert response.is_rendered is False


def test_index_view_with_events(rf):  # noqa: D103
    # GIVEN a couple mock events
    events = EventFactory.build_batch(5)

    with patch.object(IndexView, 'get_queryset', return_value=events):

        url = reverse('index')
        request = rf.get(url)
        response = IndexView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'index.html'


def test_index_view_displays_event_titles_and_venues(rf):  # noqa: D103
    events = EventFactory.build_batch(5)

    with patch.object(IndexView, 'get_queryset', return_value=events):

        url = reverse('index')
        request = rf.get(url)
        response = IndexView.as_view()(request)

        response.render()
        content = response.rendered_content

        # AND the event titles are shown and linked
        assert events[0].title in content
        assert events[0].venue.name in content
        assert events[0].date.strftime("%d/%m") in content
        assert events[0].get_absolute_url() in content

        create_url = reverse('event_create')
        assert 'add_event' in content
        assert create_url in content

        delete_url = reverse('event_delete', args=[str(events[0].id)])
        assert 'delete_event' in content
        assert delete_url in content


def test_event_detail_view(rf):  # noqa: D103
    event = EventFactory.build()

    with patch.object(EventDetailView, 'get_object', return_value=event):

        url = reverse('event_detail', args=[str(event.id)])

        request = rf.get(url)
        response = EventDetailView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'event_detail.html'

        content = response.rendered_content
        assert event.title in content


def test_event_create_view(rf):  # noqa: D103

    url = reverse('event_create')

    request = rf.get(url)
    response = EventCreateView.as_view()(request)
    assert response.template_name[0] == 'model_form.html'

    response.render()
    assert 'submit' in response.rendered_content


def test_event_update_view(rf):  # noqa: D103
    event = EventFactory.build()

    with patch.object(EventUpdateView, 'get_object', return_value=event):

        url = reverse('event_update', args=[str(event.id)])
        request = rf.get(url)

        response = EventUpdateView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'model_form.html'

        response.render()


def test_event_delete_view(rf):  # noqa: D103
    event = EventFactory.build()

    with patch.object(EventDeleteView, 'get_object', return_value=event):

        url = reverse('event_delete', args=[str(event.id)])
        request = rf.get(url)

        response = EventDeleteView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'model_delete.html'

        response.render()


def test_event_list_view(rf):  # noqa: D103
    events = EventFactory.build_batch(5)

    # GIVEN a couple mock events
    with patch.object(EventListView, 'get_queryset', return_value=events):

        url = reverse('event_list')
        request = rf.get(url)
        response = EventListView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'event_list.html'


""" VENUE VIEWS """
def test_venue_list_view(rf):  # noqa: D103, E302
    venues = VenueFactory.build_batch(5)

    # GIVEN a couple mock venues
    with patch.object(VenueListView, 'get_queryset', return_value=venues):

        url = reverse('venue_list')
        request = rf.get(url)
        response = VenueListView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'venue_list.html'

        response.render()
        content = response.rendered_content

        for venue in venues:
            assert venue.name in content


def test_venue_create_view(rf):  # noqa: D103

    url = reverse('venue_create')

    request = rf.get(url)
    response = VenueCreateView.as_view()(request)
    assert response.template_name[0] == 'model_form.html'

    response.render()
    assert 'submit' in response.rendered_content


def test_venue_update_view(rf):  # noqa: D103
    venue = VenueFactory.build()

    with patch.object(VenueUpdateView, 'get_object', return_value=venue):

        url = reverse('venue_update', args=[str(venue.id)])
        request = rf.get(url)
        response = VenueUpdateView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'model_form.html'

        response.render()


def test_venue_delete_view(rf):  # noqa: D103
    venue = VenueFactory.build()

    with patch.object(VenueDeleteView, 'get_object', return_value=venue):

        url = reverse('venue_delete', args=[0])
        request = rf.get(url)

        response = VenueDeleteView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'model_delete.html'

        response.render()