"""Unit tests for calendar views."""
from django.urls import reverse

from mock import patch

from reggae_cdmx.factories import EventFactory

from reggae_cdmx.views import (EventCreateView, EventDeleteView,
                               EventDetailView, EventListView,
                               EventUpdateView)


def test_index_view_with_no_events(rf):
    # GIVEN the home page
    url = reverse('index')

    # WHEN calling
    request = rf.get(url)
    response = EventListView.as_view()(request)

    # THEN it's there,
    assert response.status_code == 200
    assert response.template_name[0] == 'index.html'
    assert response.is_rendered is False


def test_index_view_with_events(rf):
    # GIVEN a couple mock events
    events = EventFactory.build_batch(5)

    with patch.object(EventListView, 'get_queryset', return_value=events):

        url = reverse('index')
        request = rf.get(url)
        response = EventListView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'index.html'


def test_index_view_displays_event_titles_and_venues(rf):
    events = EventFactory.build_batch(5)

    with patch.object(EventListView, 'get_queryset', return_value=events):

        url = reverse('index')
        request = rf.get(url)
        response = EventListView.as_view()(request)

        response.render()
        content = response.rendered_content

        # AND the event titles are shown and linked
        assert events[0].title in content
        assert events[0].venue in content
        assert events[0].date.strftime("%d/%m") in content
        assert events[0].get_absolute_url() in content

        create_url = reverse('create')
        assert 'add_event' in content
        assert create_url in content

        delete_url = reverse('delete', args=[str(events[0].id)])
        assert 'delete_event' in content
        assert delete_url in content


def test_event_detail_view(rf):
    event = EventFactory.build()

    with patch.object(EventDetailView, 'get_object', return_value=event):

        url = reverse('detail', args=[str(event.id)])

        request = rf.get(url)
        response = EventDetailView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'event_detail.html'

        content = response.rendered_content
        assert event.title in content


def test_event_create_view(rf):

    url = reverse('create')

    request = rf.get(url)
    response = EventCreateView.as_view()(request)
    assert response.template_name[0] == 'event_form.html'

    response.render()
    assert 'submit' in response.rendered_content


def test_event_update_view(rf):
    event = EventFactory.build()

    with patch.object(EventUpdateView, 'get_object', return_value=event):

        url = reverse('update', args=[str(event.id)])
        request = rf.get(url)

        response = EventUpdateView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'event_form.html'

        response.render()


def test_event_delete_view(rf):
    event = EventFactory.build()

    with patch.object(EventDeleteView, 'get_object', return_value=event):

        url = reverse('delete', args=[str(event.id)])
        request = rf.get(url)

        response = EventDeleteView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'event_confirm_delete.html'

        response.render()
