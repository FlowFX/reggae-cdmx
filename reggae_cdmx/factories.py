"""Model factories for calendar models."""

from reggae_cdmx.models import Event

from factory.django import DjangoModelFactory
from faker import Faker
fake = Faker()



class EventFactory(DjangoModelFactory):
    """ModelFactory for the Potato object."""

    class Meta:  # noqa
        model = Event

    title = fake.sentence(nb_words=4, variable_nb_words=True)

