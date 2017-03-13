"""Model factories for calendar app."""

from reggae_cdmx.models import Event

import factory
from factory.django import DjangoModelFactory


def faker(provider):
    """Create localized factory.Faker function."""
    return factory.Faker(provider, locale='es_MX')


class EventFactory(DjangoModelFactory):
    """ModelFactory for the Potato object."""

    class Meta:  # noqa
        model = Event

    id = factory.Sequence(lambda n: n+1)
    title = faker('name')
    date = faker('date_object')

