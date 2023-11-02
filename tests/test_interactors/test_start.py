from unittest.mock import Mock, patch, AsyncMock

import pytest

from entities.entities import UserBalance
from use_cases.start import StartInteractor


@pytest.fixture()
def bot_user():
    with patch('use_cases.start.BotUser') as b:
        b.return_value = Mock()
        yield b


@pytest.mark.asyncio
async def test_start(db_session, bot_user):
    result = await StartInteractor(db_session).execute(bot_user)

    assert not result.startswith('Здравствуйте, ')
