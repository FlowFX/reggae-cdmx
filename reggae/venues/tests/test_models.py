"""Unit tests for venues.models."""

from reggae.venues.factories import VenueFactory
from reggae.venues.models import Venue

import pytest


@pytest.mark.django_db
def test_venue_factory():  # noqa: D103
    # GIVEN an empty database
    assert Venue.objects.count() == 0

    venue = VenueFactory.build()
    venue.name = 'five'
    venue.save()

    assert Venue.objects.count() == 1

    venue = Venue.objects.first()
    assert venue.name == 'five'
