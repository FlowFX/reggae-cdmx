import pytest



from reggae.venues.factories import VenueFactory

from reggae.venues.models import Venue


@pytest.mark.django_db
def test_venue_factory():
    # GIVEN an empty database
    assert Venue.objects.count() == 0

    venue = VenueFactory.build()
    venue.name = 'five'
    venue.save()

    assert Venue.objects.count() == 1

    venue = Venue.objects.first()
    assert venue.name == 'five'
