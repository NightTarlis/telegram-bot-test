from typing import Optional
from unittest.mock import Mock, AsyncMock

import pytest
from faker import Faker

from entities.dto import UserDTO, MessageDTO

fake = Faker()


@pytest.fixture
def db_session():
    return AsyncMock()


@pytest.fixture
def logger():
    return Mock()


@pytest.fixture
def user_factory():
    def factory(
            user_id: Optional[int] = None,
            first_name: Optional[str] = None,
            username: Optional[str] = None,
            full_name: Optional[str] = None,
    ):
        return UserDTO(
            id=user_id or fake.random_int(max=2_000_000_000),
            first_name=first_name or fake.word(),
            username=username or fake.word(),
            full_name=full_name or fake.word(),
        )
    return factory


@pytest.fixture
def message_factory():
    def factory(
            message_id: Optional[int] = None,
            external_user_id: Optional[str] = None,
            chat_id: Optional[str] = None,
            text: Optional[str] = None,
    ):
        return MessageDTO(
            id=message_id or fake.random_int(max=2_000_000_000),
            external_user_id=external_user_id or fake.random_int(max=2_000_000_000),
            chat_id=chat_id or fake.random_int(max=2_000_000_000),
            text=text or fake.word(),
        )
    return factory
