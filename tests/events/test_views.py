"""Unit tests for events views."""
from app.events import factories, views

from django.urls import reverse

from mock import MagicMock

from ..conftest import TEST_DIR, today, tomorrow, yesterday


class TestHomePage:  # noqa: D101

    def test_home_page_shows_existing_events(self, client, mocker):  # noqa: D102
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

    def test_home_page_shows_only_future_events(self, db, rf, mocker):  # noqa: D102
        # GIVEN a past event
        past_event = factories.EventFactory.create(date=yesterday())

        # AND a current event
        current_event = factories.EventFactory.create(date=today())

        # AND a future event
        future_event = factories.EventFactory.create(date=tomorrow())

        # WHEN calling the home page
        url = reverse('index')
        request = rf.get(url)
        response = views.IndexView.as_view()(request)
        context = response.context_data

        # THEN the context only includes the current and future dates
        assert past_event not in context['events']
        assert current_event in context['events']
        assert future_event in context['events']

        # AND the current event comes before the future event in the list
        assert list(context['events']).index(current_event) < list(context['events']).index(future_event)


class TestEventsListView:  # noqa: D101

    def test_events_list_shows_existing_events(self, client, mocker):  # noqa: D102
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


class TestEventsDetailView:  # noqa: D101

    def test_event_detail_view_shows_event_details(self, client, mocker):  # noqa: D102
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

    def test_event_detail_view_works_without_an_event_venue(self, client, mocker):  # noqa: D102
        """Regression test for the case that an event has no venue, yet."""
        # GIVEN an existing event with no venue
        event = factories.EventFactory.build(
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

    def test_event_update_view_GET(self, db, client, authenticated_user, mocker):  # noqa: D102
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

    def test_post_request_redirects_to_event_list(self, client, authenticated_user, mocker):  # noqa: D102
        # GIVEN an existing event
        event = factories.EventFactory.build(title='Here We Go Again')
        mocker.patch.object(views.EventUpdateView, 'get_object', return_value=event)

        # WHEN updating the event via POST request
        url = reverse('events:update', args=[str(event.id)])
        data = {'title': event.title, 'date': tomorrow()}
        response = client.post(url, data)

        # THEN it redirects to the events list
        assert response.status_code == 302
        assert response.url == reverse('events:list')


class TestEventsDeleteView:  # noqa: D101

    def test_event_delete_view_GET(self, client, authenticated_user, mocker):  # noqa: D102
        # GIVEN an existing event
        event = factories.EventFactory.build()
        mocker.patch.object(views.EventDeleteView, 'get_object', return_value=event)

        # WHEN calling the delete view via GET
        url = reverse('events:delete', args=[str(event.id)])
        response = client.get(url)

        # THEN it's there
        assert response.status_code == 200
        assert response.template_name[0] == 'model_delete.html'

    def test_success_post_req_redirects_to_events_list(self, client, authenticated_user, mocker):  # noqa: D102
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

    def test_post_req_cancel_button_works(self, client, authenticated_user, mocker):  # noqa: D102
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
