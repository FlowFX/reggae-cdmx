"""Utility functions."""

import re


def assertRegex(text, regex):
    """Assert regular expression match."""
    text = str(text)
    p = re.compile(regex)
    m = p.match(text)

    assert m is not None, '{0} does not match {1}'.format(text, regex)
