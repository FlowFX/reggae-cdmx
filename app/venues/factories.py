"""Model factories for venues app."""
import factory
from factory.django import DjangoModelFactory

from .models import Venue


def faker(provider, **kwargs):
    """Create localized factory.Faker function."""
    return factory.Faker(provider, locale='es_MX', **kwargs)


class VenueFactory(DjangoModelFactory):
    """ModelFactory for the Venue object."""

    class Meta:  # noqa
        model = Venue

    id = factory.Sequence(lambda n: n+1)
    name = faker('name_female')
