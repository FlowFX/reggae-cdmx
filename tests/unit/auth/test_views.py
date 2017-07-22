"""Integration tests for auth views."""
from django.urls import reverse

import pytest


@pytest.mark.parametrize(
    'name, status_code',
    [('login', 200),
     ('logout', 200),
     ])
def test_authentication_pages(client, name, status_code):  # noqa: D103
    # GIVEN a logged out user
    # WHEN calling the page
    url = reverse(name)
    response = client.get(url)

    # THEN it's there
    assert response.status_code == status_code
