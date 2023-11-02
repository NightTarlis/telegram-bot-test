from unittest.mock import Mock, patch, AsyncMock

import pytest

from entities.entities import UserRequestStatusEnum, ExchangeRequest
from use_cases.uncategorized import UncategorizedInteractor


@pytest.fixture
def db_session():
    return Mock()


@pytest.fixture
def logger():
    return Mock()


@pytest.fixture()
def exchange_request_repository():
    with patch('use_cases.uncategorized.ExchangeRequestRepository') as er:
        er.return_value = Mock(
            create_exchange_request=AsyncMock(),
        )
        yield er


@pytest.mark.asyncio
async def test_success(exchange_request_repository, db_session, logger):
    result = await UncategorizedInteractor(db_session).execute(1, 1, 'test', 1)
    assert result == 'Ваше сообщение зарегистрировано и в скором времени мы вернемся к вам с ответом.'

    entity = ExchangeRequest(
        msg_id=1,
        external_user_id=1,
        chat_id=1,
        status=UserRequestStatusEnum.need_moderation.value,
        msg_text='test'
    )

    exchange_request_repository.return_value.create_exchange_request.assert_called_with(entity)
