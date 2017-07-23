"""Pytest fixtures."""
from selenium import webdriver

from app.events.factories import EventFactory

import pytest


@pytest.fixture(scope="session")
def browser():
    """Yield a Selenium browser instance."""
    browser = webdriver.PhantomJS(desired_capabilities={
        'phantomjs.page.settings.loadImages': 'false',
    })

    browser.implicitly_wait(3)

    yield browser

    browser.quit()


@pytest.fixture(scope="session")
def testdata():
    """Fill database with test events."""
    EventFactory.create_batch(10)


@pytest.fixture()
def authentication(live_server, browser, cookie):
    # https://stackoverflow.com/a/22497239/6476946

    browser.get(live_server.url + '/admin/')  # Selenium will set cookie domain based on current page domain
    browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
    browser.refresh()  # Need to update page for logged in user
    browser.get(live_server.url + '/admin/')
