"""Unit tests for events views."""
from datetime import date

from app.events import factories, views

from django.urls import reverse

from mock import MagicMock


class TestHomePage:

    def test_home_page_shows_existing_events(self, client, mocker):  # noqa: D103
        # GIVEN a couple events
        events = factories.EventFactory.build_batch(5)
        mocker.patch.object(views.IndexView, 'get_queryset', return_value=events)

        # WHEN calling the home page
        url = reverse('index')
        response = client.get(url)

        # THEN it's there,
        assert response.status_code == 200
        assert response.template_name[0] == 'index.html'

        # AND the event titles are shown and linked
        content = response.content.decode()
        assert events[0].title in content
        assert events[0].venue.name in content
        assert events[0].date.strftime("%d/%m") in content
        assert events[0].get_absolute_url() in content


class TestEventsListView:

    def test_events_list_shows_existing_events(self, client, mocker):  # noqa: D103
        # GIVEN a couple events
        events = factories.EventFactory.build_batch(5)
        mocker.patch.object(views.EventListView, 'get_queryset', return_value=events)

        # WHEN calling the events list
        url = reverse('events:list')
        response = client.get(url)

        # THEN it's there,
        assert response.status_code == 200
        assert response.template_name[0] == 'events/event_list.html'

        # AND the event titles are shown and linked
        content = response.content.decode()
        assert events[0].title in content
        assert events[0].venue.name in content
        assert events[0].date.strftime("%d/%m") in content
        assert events[0].get_absolute_url() in content


class TestEventsDetailView:

    def test_event_detail_view_shows_event_details(self, client, mocker):  # noqa: D103
        # GIVEN an existing event
        event = factories.EventFactory.build()
        mocker.patch.object(views.EventDetailView, 'get_object', return_value=event)

        # WHEN callint the detail view
        url = reverse('events:detail', args=[str(event.id)])
        response = client.get(url)

        # THEN it's there
        assert response.status_code == 200
        assert response.template_name[0] == 'events/event_detail.html'

        # AND the event dtails are shown
        content = response.content.decode()
        assert event.title in content
        assert event.venue.name in content
        assert event.date.strftime("%d/%m") in content


class TestEventsCreateView:

    def test_events_create_view_returns_200_on_get_request(self, client, authenticated_user):  # noqa: D103
        # GIVEN any state
        # WHEN requesting the event create view
        url = reverse('events:create')
        response = client.get(url)

        # THEN it's there
        assert response.status_code == 200
        assert response.template_name[0] == 'model_form.html'

        # AND there is a submit button
        assert 'submit' in response.content.decode()

    def test_events_create_view_redirects_to_list_view_on_post_request(self, db, client, authenticated_user, mocker):  # noqa: D103
        # GIVEN any state
        mocker.patch('app.events.models.Event.save', MagicMock(name="save"))

        # WHEN creating a new event via POST request
        url = reverse('events:create')
        data = {'title': 'Xochimilco goes Large',
                'date': date(2017, 8, 2),
                'venue': '',
                }
        response = client.post(url, data=data)

        # THEN we get redirected to the events list
        assert response.status_code == 302
        assert response.url == reverse('events:list')


def test_event_update_view_GET(db, client, authenticated_user, mocker):  # noqa: D103
    # TODO: why do we need the databse here?!
    # GIVEN an existing event
    event = factories.EventFactory.build(title='Here We Go Again')
    mocker.patch.object(views.EventUpdateView, 'get_object', return_value=event)

    # WHEN calling the update view via GET request
    url = reverse('events:update', args=[str(event.id)])
    response = client.get(url)

    # THEN it's there
    assert response.status_code == 200
    assert response.template_name[0] == 'model_form.html'

    # AND it shows the event detials
    content = response.content.decode()
    assert event.title in content


def test_event_update_view_POST_redirects_to_event_list(db, client, authenticated_user, mocker):  # noqa: D103
    # TODO: why do we need the databse here?!
    # GIVEN an existing event
    event = factories.EventFactory.build(title='Here We Go Again')
    mocker.patch.object(views.EventUpdateView, 'get_object', return_value=event)

    # WHEN updating the event via POST request
    url = reverse('events:update', args=[str(event.id)])
    data = {'title': event.title, 'date': date(2019, 8, 5)}
    response = client.post(url, data)

    # THEN it redirects to the events list
    assert response.status_code == 302
    assert response.url == reverse('events:list')


def test_event_delete_view_GET(client, authenticated_user, mocker):  # noqa: D103
    # GIVEN an existing event
    event = factories.EventFactory.build()
    mocker.patch.object(views.EventDeleteView, 'get_object', return_value=event)

    # WHEN calling the delete view via GET
    url = reverse('events:delete', args=[str(event.id)])
    response = client.get(url)

    # THEN it's there
    assert response.status_code == 200
    assert response.template_name[0] == 'model_delete.html'


def test_event_delete_view_POST_redirects_to_events_list(client, authenticated_user, mocker):  # noqa: D103
    # GIVEN an existing event
    event = factories.EventFactory.build()
    mocker.patch.object(views.EventDeleteView, 'get_object', return_value=event)
    mocker.patch('app.events.models.Event.delete', MagicMock(name="delete"))

    # WHEN calling the delete view via POST request
    url = reverse('events:delete', args=[str(event.id)])
    response = client.post(url)

    # THEN we get redirected to the events list
    # TODO: check for success message
    assert response.status_code == 302
    assert response.url == reverse('events:list')


def test_event_delete_view_POST_cancel_button_works(client, authenticated_user, mocker):  # noqa: D103
    # GIVEN an existing event
    event = factories.EventFactory.build()
    mocker.patch.object(views.EventDeleteView, 'get_object', return_value=event)

    # WHEN calling the delete view via POST request, without db or mocks
    url = reverse('events:delete', args=[str(event.id)])
    response = client.post(url, data={'cancel': 'Cancel'})

    # THEN we get redirected to the events list
    # TODO: check for success message
    assert response.status_code == 302
    assert response.url == reverse('events:list')
