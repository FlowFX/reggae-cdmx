from selenium import webdriver

from reggae.events.factories import EventFactory

import pytest


@pytest.fixture(scope="session")
def browser():
    browser = webdriver.PhantomJS(desired_capabilities={
        'phantomjs.page.settings.loadImages': 'false',
    })

    browser.implicitly_wait(3)

    yield browser

    browser.quit()


@pytest.fixture(scope="session")
def testdata():
    EventFactory.create_batch(10)