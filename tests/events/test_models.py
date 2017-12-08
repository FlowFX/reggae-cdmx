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
