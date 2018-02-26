"""Unit tests for events models."""
import datetime

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


def test_event_has_slug(db):  # noqa: D103
    # GIVEN an event
    e = EventFactory.build(
        title='One Happy Family',
        date=datetime.date(2018, 1, 1),
        venue=None,
        )
    assert e.slug == ''

    # WHEN saving the event
    e.save()

    # THEN it gets a slug generated from its date and title
    assert e.slug == '2018-01-01-one-happy-family'


def test_event_slug_gets_updated_on_date_change(db):  # noqa: D103
    # GIVEN an event
    e = EventFactory.create(
        date=datetime.date(2018, 1, 1),
        venue=None,
        )

    # WHEN changing the date
    assert e.slug.startswith('2018-01-01')
    e.date = datetime.date(2018, 1, 2)
    e.save()

    # THEN the slug changes to reflect the new date
    assert e.slug.startswith('2018-01-02')
