"""Utility functions for the calendar app."""

import re


def assertRegex(text, regex):
    """Assert regular expression match."""
    text = str(text)
    p = re.compile(regex)
    m = p.match(text)

    assert m is not None, text + " does not match " + regex
