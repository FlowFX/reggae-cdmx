"""Unit tests for events views."""
import datetime

from app.events import factories, views

from django.urls import reverse

from ..conftest import TEST_DIR, today, tomorrow, yesterday


class TestHomePage:
    """Test events.views.HomePage on '/'."""

    url = reverse('index')

    def test_home_page_context_provides_structured_calendar_of_events(self, client, mocker):  # noqa: D102
        # GIVEN two events on the same day
        date = today()

        year = date.year
        month = date.strftime('%B')
        week = date.isocalendar()[1]
        day = date.isocalendar()[2]

        events = [
            factories.EventFactory.build(id=9998, date=date, title='First Event').__dict__,  # today
            factories.EventFactory.build(id=9999, date=date).__dict__,  # also today
        ]
        events[1]['venue__name'] = 'My Venue'
        mocker.patch.object(views.HomePage, 'get_queryset', return_value=events)

        # WHEN requesting the home page
        response = client.get(self.url)

        # THEN the view context provides a structured calendar of events
        calendar = response.context_data['calendar']
        this_day = calendar[year]['months'][month]['weeks'][week]['days'][day]

        assert this_day['date'] == today()
        assert this_day['events'][0]['id'] == 9998
        assert this_day['events'][0]['title'] == 'First Event'

        assert this_day['events'][1]['id'] == 9999
        assert this_day['events'][1]['url']
        assert this_day['events'][1]['venue__name']

    def test_home_page_shows_existing_events(self, db, client, mocker):  # noqa: D102
        # GIVEN an event
        event = factories.EventFactory.create()

        # WHEN calling the home page
        response = client.get(self.url)

        # THEN it's there,
        assert response.status_code == 200
        assert response.template_name[0] == 'index.html'

        # AND the event title is shown and linked
        content = response.content.decode()
        assert event.title in content
        assert event.venue.name in content
        assert event.date.strftime("%d/%m") in content
        assert f'/events/{event.id}/' in content

    def test_home_page_only_shows_future_events(self, db, rf):  # noqa: D102
        # GIVEN only a past event
        factories.EventFactory.create(date=yesterday())

        # WHEN making a GET request to the home page
        request = rf.get(self.url)
        response = views.HomePage.as_view()(request)

        # THEN the calendar in the context is empty
        assert response.context_data['calendar'] == {}


class TestEventsListView:
    """Test events.views.EventListView on '/events/'."""

    url = reverse('events:list')

    def test_events_list_shows_existing_events(self, client, authenticated_user, mocker):  # noqa: D102
        # GIVEN a couple events
        events = factories.EventFactory.build_batch(2, slug='i-am-a-slug')
        mocker.patch.object(views.EventListView, 'get_queryset', return_value=events)

        # WHEN calling the events list
        response = client.get(self.url)

        # THEN it's there,
        assert response.status_code == 200
        assert response.template_name[0] == 'events/event_list.html'

        # AND the event titles are shown and linked
        content = response.content.decode()
        for event in events:
            assert event.title in content
            assert event.venue.name in content
            assert event.date.strftime("%d/%m") in content
            assert event.get_absolute_url() in content

    def test_anonymous_user_cant_access_events_list(self, client, mocker):  # noqa: D102
        # GIVEN any state
        mocker.patch.object(views.EventListView, 'get_queryset', return_value=None)

        # WHEN calling the events list as an anonymous user
        response = client.get(self.url)

        # THEN it redirects to the login page
        assert response.status_code == 302
        assert response.url.startswith(reverse('account_login'))


class TestEventsDetailView:  # noqa: D101

    def test_event_detail_url_uses_event_slug(self, db):  # noqa: D102
        event = factories.EventFactory.create(
            date=datetime.date(2018, 1, 1),
            venue=None,
            )

        url = reverse('events:detail', kwargs={'slug': event.slug})
        assert '2018-01-01' in url

    def test_event_absolute_url_uses_event_slug(self, db):  # noqa: D102
        event = factories.EventFactory.create(
            date=datetime.date(2018, 1, 1),
            venue=None,
            )

        assert reverse('events:detail', kwargs={'slug': event.slug}) == event.get_absolute_url()

    def test_anonymous_user_can_access_event_detail(self, client, mock_event):  # noqa: D102
        # GIVEN an existing event
        event = mock_event

        # WHEN requesting the detail view as an anonymous user
        url = reverse('events:detail', args=[str(event.id)])
        response = client.get(url)

        # THEN it's there
        assert response.status_code == 200
        assert response.template_name[0] == 'events/event_detail.html'

    def test_event_detail_view_shows_event_details(self, client, mock_event):  # noqa: D102
        # GIVEN an existing event
        event = mock_event

        # WHEN callint the detail view
        url = reverse('events:detail', args=[str(event.id)])
        response = client.get(url)

        # THEN the event dtails are shown
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

    url = reverse('events:create')

    def test_anonymous_user_cant_access_event_create_view(self, client):  # noqa: D102
        # GIVEN any state
        # WHEN requesting the event create view as an anonymous user
        response = client.get(self.url)

        # THEN she does not get access
        assert response.status_code == 302
        assert response.url.startswith(reverse('account_login'))

    def test_events_create_view_returns_200_on_get_request(self, client, authenticated_user):  # noqa: D102
        # GIVEN any state
        # WHEN requesting the event create view as an authenticated user
        response = client.get(self.url)

        # THEN it's there
        assert response.status_code == 200
        assert response.template_name[0] == 'events/event_form.html'

    def test_events_create_redirects_to_detail_view_on_post_request(self, db, client, authenticated_user):\
        # noqa: D102
        # GIVEN any state
        # WHEN creating a new event via POST request
        data = {'title': 'Xochimilco goes Large',
                'date': tomorrow(),
                'venue': '',
                }
        response = client.post(self.url, data=data)

        # THEN we get redirected to the event detail
        assert response.status_code == 302
        assert response.url.endswith('goes-large/')

    def test_events_create_can_upload_flyer_image(self, db, client, authenticated_user):  # noqa: D102
        # GIVEN any state
        # WHEN creating an event with a flyer image
        with open(TEST_DIR + '/data/test_flyer.jpg', 'rb') as flyer:
            data = {'title': 'Xochimilco goes Large',
                    'date': tomorrow(),
                    'venue': '',
                    'flyer_image': flyer,
                    }
            client.post(self.url, data=data)

        # THEN the image file gets saved into the media folder
        e = factories.Event.objects.get(title='Xochimilco goes Large')
        assert e.flyer_image.url.endswith('test_flyer.jpg')


class TestEventsUpdateView:  # noqa: D101

    def test_anonymous_user_cant_edit_events(self, client, mock_event):  # noqa: D102
        # GIVEN an existing event
        event = mock_event

        # WHEN calling the update view as an anonymous user
        url = reverse('events:update', args=[str(event.id)])
        response = client.get(url)

        # THEN she does not get access
        assert response.status_code == 302
        assert response.url.startswith(reverse('account_login'))

    def test_event_update_view_GET(self, client, authenticated_user, mock_event):  # noqa: D102
        # GIVEN an existing event
        event = mock_event

        # WHEN calling the update view via GET request
        url = reverse('events:update', args=[str(event.id)])
        response = client.get(url)

        # THEN it's there
        assert response.status_code == 200
        assert response.template_name[0] == 'events/event_form.html'

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

    def test_anonymous_user_cant_delete_events(self, client, mock_event):  # noqa: D102
        # GIVEN an existing event
        event = mock_event

        # WHEN calling the delete view as an anonymous user
        url = reverse('events:delete', args=[str(event.id)])
        response = client.get(url)

        # THEN it redirects to the login page
        assert response.status_code == 302
        assert response.url.startswith(reverse('account_login'))

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
