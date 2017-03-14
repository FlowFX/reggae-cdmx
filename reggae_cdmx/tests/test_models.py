"""Unit tests for calendar models."""
import pytest

from ..models import Event, Venue
from ..factories import EventFactory, VenueFactory


@pytest.mark.django_db
def test_event_factory():
    # GIVEN an empty database
    assert Event.objects.count() == 0

    event = EventFactory.build()
    event.title = 'five'
    event.save()

    assert Event.objects.count() == 1

    event = Event.objects.first()
    assert event.title == 'five'


@pytest.mark.django_db
def test_venue_factory():
    # GIVEN an empty database
    assert Venue.objects.count() == 0

    venue = VenueFactory.build()
    venue.name = 'five'
    venue.save()

    assert Venue.objects.count() == 1

    venue = Venue.objects.first()
    assert venue.name == 'five'
