"""Unit tests for calendar views."""
from django.urls import reverse
from mock import patch, MagicMock

from reggae.events.factories import EventFactory
from reggae.events.views import (IndexView,
                                 EventCreateView, EventDeleteView,
                                 EventDetailView, EventListView,
                                 EventUpdateView,
                                 )

from datetime import date

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

        create_url = reverse('events:create')
        assert 'add_event' in content
        assert create_url in content

        delete_url = reverse('events:delete', args=[str(events[0].id)])
        assert 'delete_event' in content
        assert delete_url in content


def test_event_detail_view(rf):  # noqa: D103
    event = EventFactory.build()

    with patch.object(EventDetailView, 'get_object', return_value=event):

        url = reverse('events:detail', args=[str(event.id)])

        request = rf.get(url)
        response = EventDetailView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'events/event_detail.html'

        content = response.rendered_content
        assert event.title in content


def test_event_create_view_GET(rf):  # noqa: D103

    url = reverse('events:create')

    request = rf.get(url)
    response = EventCreateView.as_view()(request)
    assert response.template_name[0] == 'model_form.html'

    response.render()
    assert 'submit' in response.rendered_content


@patch('reggae.events.models.Event.save', MagicMock(name="save"))
def test_event_create_view_POST(client):  # noqa: D103

    # GIVEN any state
    # WHEN creating a new event
    url = reverse('events:create')
    data = {'title': 'Xochimilco goes Large',
            'date': date(2017, 8, 20),
            'venue': None,
            }
    response = client.post(url, data=data)
    # response = EventCreateView.as_view()(request)

    # THEN we get redirected to the events list
    # assert response.url == reverse('events:list')
    # assert response.status_code == 302


def test_event_update_view(rf):  # noqa: D103
    event = EventFactory.build()

    with patch.object(EventUpdateView, 'get_object', return_value=event):

        url = reverse('events:update', args=[str(event.id)])
        request = rf.get(url)

        response = EventUpdateView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'model_form.html'

        response.render()


def test_event_delete_view_GET(rf):  # noqa: D103
    event = EventFactory.build()

    with patch.object(EventDeleteView, 'get_object', return_value=event):

        url = reverse('events:delete', args=[str(event.id)])
        request = rf.get(url)

        response = EventDeleteView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'model_delete.html'

        response.render()


@patch('reggae.events.models.Event.delete', MagicMock(name="delete"))
def test_event_delete_view_POST(client, rf):  # noqa: D103
    event = EventFactory.build()

    with patch.object(EventDeleteView, 'get_object', return_value=event):

        url = reverse('events:delete', args=[0])
        response = client.post(url)

        # TODO: add messages middleware to request factory
        # request = rf.post(url)
        # response = EventDeleteView.as_view()(request)

        assert response.status_code == 302
        assert response.url == reverse('events:list')


def test_event_list_view(rf):  # noqa: D103
    events = EventFactory.build_batch(5)

    # GIVEN a couple mock events
    with patch.object(EventListView, 'get_queryset', return_value=events):

        url = reverse('events:list')
        request = rf.get(url)
        response = EventListView.as_view()(request)

        assert response.status_code == 200
        assert response.template_name[0] == 'events/event_list.html'

        response.render()
