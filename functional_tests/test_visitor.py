from reggae_cdmx.models import Event


def test_olivia_wants_to_know_where_the_party_is(live_server, browser, testdata):
    # to have something to show for, the database is filled with sample data
    # EventFactory.create_batch(10)
    event = Event.objects.first()

    # Olivia heard of this great reggae reggae_cdmx for CDMX. She visits the home page.
    browser.get(live_server.url)

    # The browser title includes the project title
    assert 'Reggae CDMX' in browser.title

    # She sees a table of future reggae_cdmx
    table = browser.find_element_by_id('events')
    rows = table.find_elements_by_tag_name('tr')

    # And the first event interests her
    assert event.title in [row.text for row in rows]

    # She clicks on the first event
    link = browser.find_element_by_class_name('event')
    link.click()

    # She gets to the detail page of the event
