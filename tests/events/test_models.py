"""Unit tests for events models."""
from app.events.factories import EventFactory
from app.events.models import Event


def test_event_factory(db):  # noqa: D103
    # GIVEN an empty database
    assert Event.objects.count() == 0

    # WHEN saving a new event instance to the database
    EventFactory.create(title='five')

    # THEN it's there
    assert Event.objects.count() == 1


def test_event_has_all_the_attributes():  # noqa: D103
    # GIVEN an event
    e = EventFactory.build()

    # THEN it has …
    assert e.title
    assert e.date
    assert e.venue
    assert e.description
    assert e.fb_event_url
