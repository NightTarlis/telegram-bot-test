from unittest.mock import Mock, AsyncMock

import pytest
from faker import Faker

fake = Faker()


@pytest.fixture
def db_session():
    return AsyncMock()


@pytest.fixture
def logger():
    return Mock()
