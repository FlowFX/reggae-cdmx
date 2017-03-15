"""Model factories for calendar app."""

from reggae_cdmx.models import Event, Venue

import factory
from factory.django import DjangoModelFactory


def faker(provider, **kwargs):
    """Create localized factory.Faker function."""
    return factory.Faker(provider, locale='es_MX', **kwargs)


class VenueFactory(DjangoModelFactory):
    """ModelFactory for the Venue object."""

    class Meta:  # noqa
        model = Venue

    id = factory.Sequence(lambda n: n+1)
    name = faker('name_female')


class EventFactory(DjangoModelFactory):
    """ModelFactory for the Event object."""

    class Meta:  # noqa
        model = Event

    id = factory.Sequence(lambda n: n+1)
    title = faker('sentence', nb_words=4)
    date = faker('date_object')
    venue = factory.SubFactory(VenueFactory)
