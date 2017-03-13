from reggae_cdmx.models import Event

from reggae_cdmx.factories import EventFactory

from reggae_cdmx.utils import assertRegex


def test_jahshua_wants_to_add_an_event(live_server, browser):
    # Jahshua knows the home page of reggae-cdmx.com
    browser.get(live_server.url)

    # The table of events is empty
    table = browser.find_element_by_id('events')
    rows = table.find_elements_by_tag_name('tr')
    assert len(rows) == 0

    # Because he is awesome, he sees the 'add event' link
    browser.find_element_by_id('add_event').click()

    assertRegex(browser.current_url, '.+/new$')
