"""Model factories for calendar app."""

import factory
from factory.django import DjangoModelFactory

from reggae.events.models import Event
from reggae.venues.factories import VenueFactory


def faker(provider, **kwargs):
    """Create localized factory.Faker function."""
    return factory.Faker(provider, locale='es_MX', **kwargs)


class EventFactory(DjangoModelFactory):
    """ModelFactory for the Event object."""

    class Meta:  # noqa
        model = Event

    id = factory.Sequence(lambda n: n+1)
    title = faker('sentence', nb_words=4)
    date = faker('date_object')
    venue = factory.SubFactory(VenueFactory)
