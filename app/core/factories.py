"""Model factories for the core app."""
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    """ModelFactory for the User object."""

    class Meta:  # noqa: D101, D106
        model = User

    username = factory.Sequence(lambda n: 'john_doe_{0}'.format(n))  # pragma: no cover
    password = make_password("password")
