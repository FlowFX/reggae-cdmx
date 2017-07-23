"""Pytest fixtures."""
from django.contrib.auth.hashers import make_password

from app.events import factories as event_factories
from app.venues import factories, views

from mock import MagicMock

import pytest


@pytest.fixture(scope="function")
def mock_venue(mocker):
    """Mock all database-related stuff of the Venue model."""
    venue = factories.VenueFactory.build()
    mocker.patch.object(views.VenueDeleteView, 'get_object', return_value=venue)
    mocker.patch.object(views.VenueDetailView, 'get_object', return_value=venue)
    mocker.patch.object(views.VenueUpdateView, 'get_object', return_value=venue)

    mocker.patch('app.venues.models.Venue.save', MagicMock(name="save"))
    mocker.patch('app.venues.models.Venue.delete', MagicMock(name="delete"))

    yield venue


@pytest.fixture()
def user():
    """Return an existing user."""
    user = event_factories.UserFactory.create(
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
