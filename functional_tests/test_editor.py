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

    # He enters the data
    browser.find_element_by_id('id_title').send_keys('Hot and wet in Xochimilco')
    # browser.find_element_by_id('id_date').send_keys('30/08/2017')
    browser.find_element_by_id('submit-id-submit').click()


    # And gets back to the calendar view
    assertRegex(browser.current_url, '.+/$')

    # Where he sees the new entry
    table = browser.find_element_by_id('events')
    rows = table.find_elements_by_tag_name('tr')
    assert len(rows) == 1


def test_jahshua_deletes_an_event(live_server, browser):

    event = EventFactory.create()

    browser.get(live_server.url)
    assert event.title in browser.page_source

    browser.find_element_by_class_name('delete_event').click()

    browser.find_element_by_id('submit-id-submit').click()

    # The entry is gone
    table = browser.find_element_by_id('events')
    rows = table.find_elements_by_tag_name('tr')
    assert len(rows) == 0


def test_jahshua_edits_an_event(live_server, browser):
    """Test editing an existing event."""

    # GIVEN one event in the database
    event = EventFactory.create()

    # WHEN loading the home page
    browser.get(live_server.url)
    assert event.title in browser.page_source

    # AND clicking the "edit" button of the first event
    browser.find_element_by_class_name('edit_event').click()

    # THEN 
    browser.find_element_by_id('id_title').clear()
    browser.find_element_by_id('id_title').send_keys('Xochimilco goes Large')

    browser.find_element_by_id('submit-id-submit').click()

    # And gets back to the calendar view
    assertRegex(browser.current_url, '.+/$')

    assert event.title not in browser.page_source
    assert 'Xochimilco' in browser.page_source


