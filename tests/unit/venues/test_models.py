"""Unit and integration tests for venues.models."""
from app.venues.factories import VenueFactory
from app.venues.models import Venue


def test_venue_factory(db):  # noqa: D103
    # GIVEN an empty database
    assert Venue.objects.count() == 0

    # WHEN saving a new venue instance to the database
    VenueFactory.create(name='five')

    # THEN it's there
    assert Venue.objects.count() == 1
