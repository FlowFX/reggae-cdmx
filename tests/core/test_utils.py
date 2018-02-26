"""Tests for the utility functions."""
from app.core.utils import environment_processor


def test_environment_processor_returns_current_environment():
    """Test the context processor that provides the current environment to the template context."""
    assert environment_processor() == {'environment': 'testing'}
