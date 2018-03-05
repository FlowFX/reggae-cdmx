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


def test_login_redirects_properly(client):  # noqa: D103
    # GIVEN any state
    # WHEN requesting the '/login/' URL
    old_url = '/login/'
    new_url = reverse('account_login')

    response = client.get(old_url)

    # THEN it redirects to Allauth's default /accounts/login/'
    assert response.status_code == 301
    assert response.url == new_url


def test_signup_returns_404(db, client):  # noqa: D103
    # GIVEN any state
    # WHEN requesting the signup page
    url = reverse('account_signup')

    response = client.get(url)

    # THEN it returns a 404
    assert response.status_code == 404
