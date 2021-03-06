"""Unit tests for utility functions."""
from app.events.utils import assertRegex

import pytest


@pytest.mark.parametrize('text, regex, assertion',
                         [('Bungalo Dub', '^Bungalo.+', True),
                          ('Bungalo Dub', '.+Dub$', True),
                          ('Bungalo Dub', 'Bungalo Dub', True),
                          ('Bungalo Dub', '^Bngalo.+', False),
                          ])
def test_assertregex(text, regex, assertion):
    """Unit test the assertRegex function."""
    if assertion is True:
        assertRegex(text, regex)
    elif assertion is False:
        with pytest.raises(AssertionError):
            assertRegex(text, regex)
