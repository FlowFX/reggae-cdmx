"""Unit tests for form validation."""
from datetime import date

from app.events.forms import EventForm

import pytest


class TestEventForm:  # noqa: D101

    @pytest.mark.parametrize(
        'title, date, venue, validity',
        [('Bungalo Dub ft. Jahshua Soundman', date(2017, 8, 20), None, True),
         ('Bungalo Dub', '', None, False),   # empty date
         ('', '20/08/2017', None, False),    # empty title
         ])
    def test_event_requires_title_and_date_but_no_venue(self, title, date, venue, validity):
        """Test form validation for EventForm."""
        form = EventForm(data={
            'title': title,
            'date': date,
            'venue': venue,
        })

        assert form.is_valid() is validity

    @pytest.mark.parametrize(
        'fb_event_url, validity',
        [('https://www.facebook.com/events/2001223273532037/', True),
         ('https://www.fakebook.com/events/2001223273532037/', False),  # typo
         ('', True),   # empty event url
         ])
    def test_event_allows_only_valid_facebook_urls_or_empty(self, fb_event_url, validity):
        """Test form validation for EventForm."""
        form = EventForm(data={
            'title': 'A title',
            'date': date(2017, 8, 20),
            'fb_event_url': fb_event_url,
        })

        assert form.is_valid() is validity
