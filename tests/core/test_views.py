"""Integration tests for auth views."""
from django.urls import reverse

import pytest


@pytest.mark.parametrize(
    'name, status_code',
    [('account_login', 200),
     ('account_logout', 302),  # gets redirected to '/'
     ])
def test_authentication_pages(db, client, name, status_code):  # noqa: D103
    # GIVEN a logged out user
    # WHEN calling the page
    url = reverse(name)
    response = client.get(url)

    # THEN it's there
    assert response.status_code == status_code
