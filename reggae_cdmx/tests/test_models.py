"""Unit tests for calendar models."""
import pytest

from ..models import Event
from ..factories import EventFactory


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
