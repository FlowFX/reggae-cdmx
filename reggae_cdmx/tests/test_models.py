"""Unit tests for calendar models."""
import pytest

from reggae_cdmx.models import Event


@pytest.mark.django_db
def test_event_factory():
    # GIVEN an empty database
    assert Event.objects.count() == 0

    event = Event()
    event.title = 'five'
    event.save()

    assert Event.objects.count() == 1

    event = Event.objects.first()
    assert event.title == 'five'
