"""Unit tests for calendar models."""
import pytest

from app.events.factories import EventFactory
from app.events.models import Event


@pytest.mark.django_db
def test_event_factory():  # noqa: D103
    # GIVEN an empty database
    assert Event.objects.count() == 0

    event = EventFactory.build()
    event.title = 'five'
    event.save()

    assert Event.objects.count() == 1

    event = Event.objects.first()
    assert event.title == 'five'
