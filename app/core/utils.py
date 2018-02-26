"""Utility functions."""
from django.conf import settings


def environment_processor(request=None):
    """Context processor that provides the current environment to the template context."""
    return {'environment': settings.ENVIRONMENT}
