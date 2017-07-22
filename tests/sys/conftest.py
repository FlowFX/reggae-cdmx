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
