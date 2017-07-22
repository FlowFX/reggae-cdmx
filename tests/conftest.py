"""Pytest fixtures."""
import pytest

from app.venues import factories, views

from mock import MagicMock


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
