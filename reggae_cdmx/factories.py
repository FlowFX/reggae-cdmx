"""Model factories for calendar app."""

from reggae_cdmx.models import Event

import factory
from factory.django import DjangoModelFactory


def faker(provider, **kwargs):
    """Create localized factory.Faker function."""
    return factory.Faker(provider, locale='es_MX', **kwargs)


class EventFactory(DjangoModelFactory):
    """ModelFactory for the Potato object."""

    class Meta:  # noqa
        model = Event

    id = factory.Sequence(lambda n: n+1)
    # title = faker('name')
    title = faker('sentence', nb_words=4)
    date = faker('date_object')

