import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_db():
    return Mock()


@pytest.fixture
def mock_api():
    return Mock()