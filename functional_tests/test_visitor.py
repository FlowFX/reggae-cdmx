from reggae_cdmx.models import Event

from reggae_cdmx.factories import EventFactory

from reggae_cdmx.utils import assertRegex


def test_olivia_wants_to_know_where_the_party_is(live_server, browser):
    # to have something to show for, the database is filled with sample data
    EventFactory.create_batch(10)
    event = Event.objects.first()

    # Olivia heard of this great reggae reggae_cdmx for CDMX. She visits the home page.
    browser.get(live_server.url)

    # The browser title includes the project title
    assert 'Reggae CDMX' in browser.title

    # She sees a table of future reggae_cdmx
    table = browser.find_element_by_id('events')
    rows = table.find_elements_by_tag_name('tr')

    # It shows all the events and their titles
    assert len(rows) == 10
    assert event.title in [row.text for row in rows]

    # She clicks on the first event
    old_url = browser.current_url
    # row = browser.find_element_by_class_name('event')
    rows[0].find_element_by_tag_name('a').click()

    # She gets to the detail page of the event. The URL is different.
    # (But we don't know how different, yet.
    new_url = browser.current_url
    assert old_url != new_url
    # assertRegex(current_url, '')

    assert event.title in browser.page_source
