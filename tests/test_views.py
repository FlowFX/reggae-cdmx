from django.urls import reverse

from potatos.models import Potato

import pytest


def test_index_view(client):
    """Test the index view using the Django test client."""

    # GIVEN the home page
    url = reverse('index')

    # WHEN calling it with the Django test client
    response = client.get(url)

    # THEN it's there,
    assert response.status_code == 200
    # the project title is visible,
    assert '<h1>Sturdy Potato</h1>' in response.content.decode()
    # and the correct template is used
    assert 'index.html' in (template.name for template in response.templates)


@pytest.mark.django_db
def test_detail_view(client):
    """Test the detail view for a Potato object with the Django test client."""

    # GIVEN a Potato object
    potato = Potato()
    potato.name = 'Eve'
    potato.variety = 'Anya'
    potato.save()

    # WHEN calling the DetailView for this object
    url = reverse('detail', kwargs={'pk': potato.id})
    response = client.get(url)

    content = response.content.decode()
    # THEN it shows the potato's ID and it's type
    assert response.status_code == 200
    assert potato.name in content
    assert potato.variety in content


@pytest.mark.django_db
def test_list_view(client):
    """Test the list view for Potato objects."""

    # GIVEN a number of potatos
    for _ in range(5):
        Potato().save()

    # WHEN calling the list view for our potatos
    url = reverse('list')
    response = client.get(url)

    content = response.content.decode()
    # THEN all existing potatos are listed
    potatos = Potato.objects.all()

    for potato in potatos:
        assert str(potato.id) in content




