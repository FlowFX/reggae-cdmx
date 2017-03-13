"""Unit tests for calendar views."""
from django.urls import reverse

from reggae_cdmx.utils import assertRegex
from mock import patch

from reggae_cdmx.factories import EventFactory

from reggae_cdmx.views import EventCreateView, EventDetailView, EventListView


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


def test_index_view_displays_event_titles(rf):
    events = EventFactory.build_batch(5)

    with patch.object(EventListView, 'get_queryset', return_value=events):

        url = reverse('index')
        request = rf.get(url)
        response = EventListView.as_view()(request)

        response.render()
        content = response.rendered_content

        # AND the event titles are shown and linked
        assert events[0].title in content
        assert events[0].date.strftime("%d/%m") in content
        assert events[0].get_absolute_url() in content

        assert 'add_event' in content


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

