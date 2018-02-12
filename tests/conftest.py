"""Pytest fixtures."""
import datetime
import os

from app.core import factories as core_factories
from app.events import factories as events_factories, views as events_views
from app.venues import factories as venues_factories, views as venues_views

from django.conf import settings
from django.contrib.auth.hashers import make_password

from mock import MagicMock

import pytest


TEST_DIR = os.path.abspath(os.path.join(settings.BASE_DIR, 'tests'))


def today():
    """Return datetime.date object of today."""
    return datetime.date.today()


def yesterday():
    """Return datetime.date object of yesterday."""
    return today() - datetime.timedelta(1)


def tomorrow():
    """Return datetime.date object of tomorrow."""
    return today() + datetime.timedelta(1)


@pytest.fixture(scope="function")
def mock_event(mocker):
    """Mock all database-related stuff of the Event model."""
    event = events_factories.EventFactory.build(id=9999, venue__id=9999)
    mocker.patch.object(events_views.EventDeleteView, 'get_object', return_value=event)
    mocker.patch.object(events_views.EventDetailView, 'get_object', return_value=event)
    mocker.patch.object(events_views.EventUpdateView, 'get_object', return_value=event)

    mocker.patch('app.events.models.Event.save', MagicMock(name="save"))
    mocker.patch('app.events.models.Event.delete', MagicMock(name="delete"))

    yield event


@pytest.fixture(scope="function")
def mock_venue(mocker):
    """Mock all database-related stuff of the Venue model."""
    venue = venues_factories.VenueFactory.build(id=9999)
    mocker.patch.object(venues_views.VenueDeleteView, 'get_object', return_value=venue)
    mocker.patch.object(venues_views.VenueDetailView, 'get_object', return_value=venue)
    mocker.patch.object(venues_views.VenueUpdateView, 'get_object', return_value=venue)

    mocker.patch('app.venues.models.Venue.save', MagicMock(name="save"))
    mocker.patch('app.venues.models.Venue.delete', MagicMock(name="delete"))

    yield venue


@pytest.fixture()
def user():
    """Return an existing user."""
    user = core_factories.UserFactory.create(
        username='testuser',
        password=make_password('password'),
    )

    return user


@pytest.fixture()
def authenticated_user(db, client, user):
    """Return an authenticated user."""
    # TODO: don't use the database here, if possible
    client.force_login(user)

    return user


@pytest.fixture()
def cookie(client, authenticated_user):
    """Return a session cookie for a logged-in user."""
    # http://django.readthedocs.io/en/1.9.x/topics/testing/tools.html#django.test.Client.force_login
    # https://stackoverflow.com/a/39742798/6476946
    client.force_login(user)
    cookie = client.cookies['sessionid']

    yield cookie
