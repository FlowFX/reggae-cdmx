"""Unit tests for events views."""
from app.events import factories, views

from django.urls import reverse

from mock import MagicMock

from ..conftest import TEST_DIR, today, tomorrow, yesterday


class TestHomePage:
    """Test events.views.HomePage on '/'."""

    def test_home_page_context_provides_structured_calendar_of_events(self, client, mocker):  # noqa: D102
        # GIVEN a event
        events = [factories.EventFactory.build(
            id=9999,
            date=today(),
            ), ]  # today
        mocker.patch.object(views.HomePage, 'get_queryset', return_value=events)

        # WHEN requesting the home page
        url = reverse('index')
        response = client.get(url)

        # THEN the view context provides a structured calendar of events
        calendar = response.context_data['calendar']

        year = today().year
        month = today().strftime('%B')
        week = today().isocalendar()[1]
        day = today().isocalendar()[2]

        assert type(calendar) is dict
        assert calendar[year]['year'] == year
        assert calendar[year]['months'][month]['month'] == month
        assert calendar[year]['months'][month]['weeks'][week]['week'] == week
        assert calendar[year]['months'][month]['weeks'][week]['days'][day]['date'] == today()
        assert calendar[year]['months'][month]['weeks'][week]['days'][day]['events'][0] == events[0]

    def test_home_page_shows_existing_events(self, client, mocker):  # noqa: D102
        # GIVEN a couple events
        events = factories.EventFactory.build_batch(3, id=9999)
        mocker.patch.object(views.HomePage, 'get_queryset', return_value=events)

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

    def test_home_page_shows_only_future_events(self, db, rf, mocker):  # noqa: D102
        # GIVEN a past event
        past_event = factories.EventFactory.create(date=yesterday(), id=9997)

class TestEventsListView:
    """Test events.views.EventListView on '/events/'."""

    def test_events_list_shows_existing_events(self, client, mocker):  # noqa: D102
        # GIVEN a couple events
        events = factories.EventFactory.build_batch(5, id=9999)
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


class TestEventsDetailView:  # noqa: D101

    def test_event_detail_view_shows_event_details(self, client, mock_event):  # noqa: D102
        # GIVEN an existing event
        event = mock_event

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

    def test_event_detail_view_works_without_an_event_venue(self, client, mocker):  # noqa: D102
        """Regression test for the case that an event has no venue, yet."""
        # GIVEN an existing event with no venue
        event = factories.EventFactory.build(
            id=9999,
            venue=None,
        )
        mocker.patch.object(views.EventDetailView, 'get_object', return_value=event)

        # WHEN callint the detail view
        url = reverse('events:detail', args=[str(event.id)])
        response = client.get(url)

        # THEN it's there
        assert response.status_code == 200


class TestEventsCreateView:  # noqa: D101

    def test_events_create_view_returns_200_on_get_request(self, client, authenticated_user):  # noqa: D102
        # GIVEN any state
        # WHEN requesting the event create view
        url = reverse('events:create')
        response = client.get(url)

        # THEN it's there
        assert response.status_code == 200
        assert response.template_name[0] == 'model_form.html'

        # AND there is a submit button
        assert 'submit' in response.content.decode()

    def test_events_create_view_redirects_to_list_view_on_post_request(self, db, client, authenticated_user, mocker):\
    # noqa: D102
        # GIVEN any state
        mocker.patch('app.events.models.Event.save', MagicMock(name="save"))

        # WHEN creating a new event via POST request
        url = reverse('events:create')
        data = {'title': 'Xochimilco goes Large',
                'date': tomorrow(),
                'venue': '',
                }
        response = client.post(url, data=data)

        # THEN we get redirected to the events list
        assert response.status_code == 302
        assert response.url == reverse('events:list')

    def test_events_create_can_upload_flyer_image(self, db, client, authenticated_user):  # noqa: D102
        # GIVEN any state
        # WHEN creating an event with a flyer image
        with open(TEST_DIR + '/data/test_flyer.jpg', 'rb') as flyer:
            url = reverse('events:create')
            data = {'title': 'Xochimilco goes Large',
                    'date': tomorrow(),
                    'venue': '',
                    'flyer_image': flyer,
                    }
            client.post(url, data=data)

        # THEN the image file gets saved into the media folder
        e = factories.Event.objects.get(title='Xochimilco goes Large')
        assert e.flyer_image.url.endswith('test_flyer.jpg')


class TestEventsUpdateView:  # noqa: D101

    def test_event_update_view_GET(self, client, authenticated_user, mock_event):  # noqa: D102
        # GIVEN an existing event
        event = mock_event

        # WHEN calling the update view via GET request
        url = reverse('events:update', args=[str(event.id)])
        response = client.get(url)

        # THEN it's there
        assert response.status_code == 200
        assert response.template_name[0] == 'model_form.html'

        # AND it shows the event detials
        content = response.content.decode()
        assert event.title in content

    def test_post_request_redirects_to_event_list(self, client, authenticated_user, mock_event):  # noqa: D102
        # GIVEN an existing event
        event = mock_event

        # WHEN updating the event via POST request
        url = reverse('events:update', args=[str(event.id)])
        data = {'title': event.title, 'date': tomorrow()}
        response = client.post(url, data)

        # THEN it redirects to the events list
        assert response.status_code == 302
        assert response.url == reverse('events:list')


class TestEventsDeleteView:  # noqa: D101

    def test_event_delete_view_GET(self, client, authenticated_user, mock_event):  # noqa: D102
        # GIVEN an existing event
        event = mock_event

        # WHEN calling the delete view via GET
        url = reverse('events:delete', args=[str(event.id)])
        response = client.get(url)

        # THEN it's there
        assert response.status_code == 200
        assert response.template_name[0] == 'model_delete.html'

    def test_success_post_req_redirects_to_events_list(self, client, authenticated_user, mock_event):  # noqa: D102
        # GIVEN an existing event
        event = mock_event

        # WHEN calling the delete view via POST request
        url = reverse('events:delete', args=[str(event.id)])
        response = client.post(url)

        # THEN we get redirected to the events list
        # TODO: check for success message
        assert response.status_code == 302
        assert response.url == reverse('events:list')

    def test_post_req_cancel_button_works(self, client, authenticated_user, mock_event):  # noqa: D102
        # GIVEN an existing event
        event = mock_event

        # WHEN calling the delete view via POST request, without db or mocks
        url = reverse('events:delete', args=[str(event.id)])
        response = client.post(url, data={'cancel': 'Cancel'})

        # THEN we get redirected to the events list
        # TODO: check for success message
        assert response.status_code == 302
        assert response.url == reverse('events:list')
