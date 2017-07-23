"""Model factories for calendar app."""
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

import factory
from factory.django import DjangoModelFactory

from .models import Event
from ..venues.factories import VenueFactory


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


class UserFactory(DjangoModelFactory):
    """ModelFactory for the User object."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'john_doe_{0}'.format(n))  # pragma: no cover
    password = make_password("password")
