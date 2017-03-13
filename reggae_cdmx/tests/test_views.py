"""Unit tests for calendar views."""
from django.urls import reverse

from reggae_cdmx.views import IndexView


def test_index_view(rf):
    # GIVEN the home page
    url = reverse('index')

    # WHEN calling
    request = rf.get(url)
    response = IndexView.as_view()(request)

    # THEN it's there,
    assert response.status_code == 200
    assert response.template_name[0] == 'index.html'
    assert response.is_rendered is False
